# Architecture

## Summary

- One process, endless loop in `workshop_changelogs/run.py`.
- Inputs: Steam Web API `ISteamRemoteStorage` (POST), Steam Community
  changelog HTML page (GET, parsed with BeautifulSoup).
- Output: one Discord webhook POST per updated mod.
- State: `config.json` (path `CONFIG_PATH`), rewritten after every pass with
  the whole `Config` object including the `cache` (mod ID -> `time_updated`).

## Module map

| Path | Responsibility |
| --- | --- |
| `workshop_changelogs/__init__.py` | Package logger |
| `workshop_changelogs/config.py` | `Config` (env vars with `config.json` fallback), `write_config()`, `first_install`; module-level singleton `config = get_config()` |
| `workshop_changelogs/run.py` | `_run()` (one pass), `run()` (loop with `sleep`), `root_run()` (logging setup, entry point) |
| `workshop_changelogs/steam/api_client.py` | `_client()` for `GetPublishedFileDetails` / `GetCollectionDetails`; `get_mod_info()`, `get_mod_info_from_collection()` |
| `workshop_changelogs/steam/change_log_parser.py` | `get_change_log()`: fetches `CHANGE_LOG_BASE_URL/<mod_id>`, returns text of the first `<p>` with a numeric `id` |
| `workshop_changelogs/discord/webhook.py` | `send_discord_message()`: builds the embed and posts it |
| `workshop_changelogs/i18n/translations.py` | `EN_MESSAGES`, `DE_MESSAGES`, `translate()` (imported as `t`) |

## Pass flow (`_run()`)

1. Fetch mod details for `MOD_IDS` and for all children of `COLLECTION_IDS`.
2. Skip entries with a falsy `result`.
3. Unknown mod: store `time_updated` in `config.cache`.
4. Send when `time_updated` differs from the cache, or `SEND_ON_STARTUP` and
   first pass of this process, or `SEND_ON_INSTALL` and the cache was empty
   at pass start.
5. After sending, update the cache; at the end set `config.started = True`
   and `write_config()`.
6. `run()` sleeps `SLEEP_INTERVAL` seconds and repeats.

## Discord message (`send_discord_message()`)

- Fixed `username` and `avatar_url`, embed title = mod title, URL = changelog
  page, colour `15258703`, one field `News` with date and changelog text,
  fixed footer.
- Returns the HTTP status code; non-2xx is only logged at debug level.

## Invariants

- `translate()` looks up `MESSAGES[config.language][message_id]`; language is
  the first two characters of `LANG`.
- All HTTP calls use `config.requests_timeout`.
- Network exceptions from `requests` are not caught; an exception ends the
  loop and the process (Docker restarts it with `restart: always`).
