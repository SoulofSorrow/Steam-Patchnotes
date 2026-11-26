@AGENTS.md

## Claude Code specifics

- Project skills live in `.claude/skills/`. Invoke the matching skill before
  starting a task it covers.
- `.claude/settings.json` allows the lint and compile checks and denies
  reading `.env` and `config.json`.
- Run `ruff check .` and `python -m compileall workshop_changelogs` before
  reporting a task as done.
