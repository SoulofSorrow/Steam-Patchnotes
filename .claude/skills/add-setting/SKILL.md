---
name: add-setting
description: Add a new configuration value to the Steam Workshop Changelog Monitor (env var with config.json fallback). Use when a feature needs a configurable value.
---

# Add a setting

Background: `docs/configuration.md`.

## Steps

1. **Config** in `Config.__init__` (`workshop_changelogs/config.py`):

   ```python
   self.<name> = os.getenv("<NAME>", _config_from_json("<name>", <default>))
   ```

   Convert types explicitly (`int(...)`; booleans: accept both `bool` and
   strings, do not copy the existing `SEND_ON_*` pattern, which turns JSON
   booleans into `False`).
2. **Usage**: read `config.<name>` from the module singleton.
3. **Template**: `.env.SAMPLE` line with an inline comment.
4. **Compose**: `- <NAME>=${<NAME>}` with a comment in
   `docker-compose.yml`.
5. **Docs**: row in `docs/configuration.md`; configuration notes in
   `README.md` and `README.de.md`; then the `document-change` skill.
6. Run `ruff check .` and `python -m compileall workshop_changelogs`.

## Rules

- `write_config()` dumps every attribute to `config.json`; a secret stored on
  `Config` ends up there. Never commit `config.json`.
- Line length 79.
