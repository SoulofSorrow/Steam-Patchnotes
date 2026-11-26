# AGENTS.md

Instructions for AI coding agents working in this repository. Tool-agnostic;
`CLAUDE.md` imports this file.

## Project

Steam Workshop Changelog Monitor (package `workshop_changelogs`): long-running
Python loop that polls the Steam Web API for Workshop mods (directly or via
collections), scrapes the latest changelog entry and posts a Discord webhook
embed when a mod was updated. Log messages in English or German.

Stack: Python (`requires-python >=3.8` in `pyproject.toml`, code uses
`X | Y` type unions, CI uses 3.12), `requests`, `beautifulsoup4`; setuptools
packaging; Docker on `python:alpine`. License per `LICENSE.md`.

## Read first

1. `docs/README.md` (index).
2. The topic doc for the area you touch:

| Area | Doc |
| --- | --- |
| Module map, polling loop, cache, invariants | `docs/architecture.md` |
| Environment variables and `config.json` | `docs/configuration.md` |
| Setup, lint, conventions | `docs/development.md` |
| Docker image, compose, CI workflows | `docs/deployment.md` |

## Commands

```bash
pip install -e '.[dev]'                   # dev install (ruff, black, isort, bandit, pre-commit)
ruff check .                              # CI lint gate
python -m compileall workshop_changelogs  # CI compile gate
workshop_changelogs                       # console script -> workshop_changelogs.run:root_run
python workshop_changelogs/run.py         # same, as in the Docker ENTRYPOINT (needs PYTHONPATH=.)
pre-commit run --all-files                # black, ruff, isort, bandit
```

There is no test suite. `README.md` mentions `tox`, but no `tox.ini` exists.

## Definition of done

- `ruff check .` and `python -m compileall workshop_changelogs` pass (CI).
- Affected topic doc in `docs/` updated.
- New file `docs/changes/YYYY-MM-DD-<slug>.md` (template in
  `.claude/skills/document-change/SKILL.md`), listed in `docs/README.md`.
- New log or Discord text: key in both `EN_MESSAGES` and `DE_MESSAGES`.
- User-visible behaviour or config changed: `README.md`, `README.de.md`,
  `.env.SAMPLE` and `docker-compose.yml` updated together.

## Hard rules

- Never commit `.env` or `config.json` (both git-ignored). `config.json` is
  written by the app and contains the webhook URL and the cache.
- `EN_MESSAGES` and `DE_MESSAGES` in
  `workshop_changelogs/i18n/translations.py` must have identical keys in the
  same order; `translate()` raises `KeyError` on a missing key.
- Environment variables take priority over `config.json`; JSON keys are the
  lowercase names (see `docs/configuration.md` for exceptions).
- Every outbound HTTP call passes `timeout=config.requests_timeout`.
- Line length 79 (ruff, black, isort config in `pyproject.toml`).
- Do not push to `main` or push `v*.*.*` tags unless the user asks (tags
  trigger image builds and a GitHub release).
- No emojis in code, logs or docs.

## Language

| Artifact | Language |
| --- | --- |
| Code, comments, docstrings | English |
| Log and Discord texts | English and German via `translate()` |
| Commit messages, `docs/`, `README.md` | English |
| `README.de.md` | German |

Commits: Conventional Commits, imperative, no tool attribution trailers.

## Project skills

Located in `.claude/skills/<name>/SKILL.md`.

| Skill | Use for |
| --- | --- |
| `add-message` | New or changed log/Discord text in both languages |
| `add-setting` | New environment variable / `config.json` key |
| `document-change` | Writing the `docs/changes/` record |
