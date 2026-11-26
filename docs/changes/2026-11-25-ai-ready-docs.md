---
date: 2026-11-25
type: docs
scope: docs, agent tooling
files: [AGENTS.md, CLAUDE.md, .claude/settings.json, .claude/skills/add-message/SKILL.md, .claude/skills/add-setting/SKILL.md, .claude/skills/document-change/SKILL.md, docs/README.md, docs/architecture.md, docs/configuration.md, docs/development.md, docs/deployment.md, docs/changes/2026-11-25-ai-ready-docs.md, README.md, README.de.md, .dockerignore]
breaking: false
---
# Agent-ready documentation and project skills

## Context

- The repository had no `docs/` folder and no instructions for AI coding
  agents. Knowledge lived in `README.md`, `.env.SAMPLE` and the code.
- Goal: an agent can find the relevant module, rules and workflow without
  reading the whole codebase.

## Change

- `docs/README.md`: index, change records, maintenance rules.
- `docs/architecture.md`: module map, pass flow, Discord payload, invariants.
- `docs/configuration.md`: env vars, `config.json` keys, precedence, parsing
  notes.
- `docs/development.md`: setup, CI checks, pre-commit, conventions.
- `docs/deployment.md`: Dockerfile, compose, CI and release workflows.
- `AGENTS.md`: tool-agnostic agent instructions.
- `CLAUDE.md`: imports `AGENTS.md`, Claude Code notes.
- `.claude/settings.json`: allows `ruff check`, `ruff format --check`,
  `python -m compileall workshop_changelogs`, `pre-commit run`; asks before
  `git push` and `docker compose up`; denies reading `.env` and
  `config.json`.
- `.claude/skills/`: `add-message`, `add-setting`, `document-change`.
- `README.md`, `README.de.md`: documentation section.
- `.dockerignore`: excludes `AGENTS.md`, `CLAUDE.md`, `.claude/`, `docs/`
  (the image uses `COPY . .`).

## Decisions

- `AGENTS.md` canonical, `CLAUDE.md` imports it.
- Existing tool config (black, isort, ruff) documented as is; no tooling
  changes in a docs-only change.
- No `release` skill: no local release tooling; tags trigger CI.

## Usage / Verification

```bash
python3 -m json.tool .claude/settings.json
ls docs docs/changes .claude/skills
ruff check .
python -m compileall workshop_changelogs
```

## Follow-ups

- Missing standard files: `Makefile` (build/test/tag targets),
  `CHANGELOG.md`, `CONTRIBUTING.md`. `LICENSE.md` exists (not `LICENSE`).
- No tests; `README.md` documents `tox`, but `tox.ini` does not exist.
- `config.py`: `.split(",")` results for `MOD_IDS` / `COLLECTION_IDS` are
  discarded, so comma-separated env values are passed as one string.
- `config.py`: JSON booleans and the default `True` for `send_on_install`
  are converted to `False`.
- `write_config()` persists `webhook_url` into `config.json`.
- `requests` exceptions are not caught; one network error ends the loop.
- `pyproject.toml` `requires-python >=3.8`, but the code uses `X | Y` type
  syntax (3.10+).
- Pre-commit pins ruff `v0.0.291` while CI installs the latest ruff; black and
  isort are configured alongside ruff.
- `README.de.md` references a non-existent `docker` directory.
