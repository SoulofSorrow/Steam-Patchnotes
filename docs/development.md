# Development

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
pre-commit install
```

Dependencies: `requirements.txt` (`beautifulsoup4`, `requests`), read
dynamically by setuptools. Dev extras: `bandit`, `black`, `isort`,
`pre-commit`, `ruff`.

## Checks

| Command | Used by |
| --- | --- |
| `ruff check .` | CI (`lint` job) |
| `python -m compileall workshop_changelogs` | CI (`lint` job) |
| `pre-commit run --all-files` | Local hooks: black 23.9.1, ruff v0.0.291, isort 5.12.0, bandit 1.7.5 |

- `pyproject.toml`: ruff `line-length = 79`, rules `B`, `C`, `E`, `F`, `W`,
  extra excludes `venv`, `__init__.py`; black and isort also at 79.
- No tests and no `tox.ini`, although `README.md` describes `tox`.

## Run locally

```bash
export DISCORD_WEBHOOK_URL=...   # or create config.json
export MOD_IDS=...
workshop_changelogs
```

## Conventions

- Logs through module loggers and `t("<key>", ...)`; no raw strings in log
  calls except debug dumps.
- Type hints on public functions (existing style), docstrings in reST field
  style (`:param:`, `:rtype:`).
