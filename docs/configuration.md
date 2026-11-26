# Configuration

Source: `workshop_changelogs/config.py`. Each value is read from the
environment first; if unset, from `config.json` (path `CONFIG_PATH`, default
`config.json` in the working directory); else the default. Template:
`.env.SAMPLE`.

| Env var | `config.json` key | Default | Purpose |
| --- | --- | --- | --- |
| `LANG` | none | `en` | Language for logs/Discord texts; first two characters (`en`, `de`). The Docker image sets `ENV LANG en` |
| `MOD_IDS` | `mod_ids` | `[]` | Workshop mod IDs, comma separated |
| `COLLECTION_IDS` | `collection_ids` | `[]` | Workshop collection IDs, comma separated |
| `DISCORD_WEBHOOK_URL` | `webhook_url` | none | Discord webhook |
| `SLEEP_INTERVAL` | `sleep_interval` | `300` | Seconds between passes (`.env.SAMPLE` uses 60) |
| `LOG_LEVEL` | `log_level` | `INFO` | Root logger level |
| `REQUESTS_TIMEOUT` | `requests_timeout` | `10` | Timeout for all HTTP calls |
| `SEND_ON_INSTALL` | `send_on_install` | `True` | Send for every mod on the first pass when the cache is empty |
| `SEND_ON_STARTUP` | `send_on_startup` | `False` | Send for every mod on the first pass of each process start |
| `CONFIG_PATH` | none | `config.json` | Path of the JSON config/cache file |

## `config.json`

- Written by `Config.write_config()` after every pass: `json.dump` of all
  `Config` attributes (including `webhook_url`, `cache`, `started`,
  `language`).
- Mounted in compose as `./config.json:/app/config.json`.
- Git-ignored. Treat it as a secret because it contains the webhook URL.

## Parsing notes (current code)

- `SEND_ON_INSTALL` / `SEND_ON_STARTUP` become `True` only when the value is
  a string equal to `true` (case-insensitive). A JSON boolean or the default
  `True` ends up as `False`.
- For string values of `MOD_IDS` / `COLLECTION_IDS` the result of
  `.split(",")` is discarded, so the raw string is passed on.

## Rules

- Secrets only in `.env` or `config.json`, never committed.
- New variables: `Config.__init__`, `.env.SAMPLE`, `docker-compose.yml`
  `environment:`, this file, both READMEs.
