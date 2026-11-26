# Deployment

## Docker image (`Dockerfile`)

- `python:alpine`, `apk upgrade`; builder stage installs `requirements.txt`
  into `/build`.
- Final stage: `ENV LANG en`, `PYTHONPATH /app`, user `app`, `COPY . .`.
- `ENTRYPOINT ["python", "workshop_changelogs/run.py"]`.
- `.dockerignore` excludes `.github`, `tests/`, `Dockerfile`, compose file,
  caches, `.git/`, plus agent docs (`AGENTS.md`, `CLAUDE.md`, `.claude/`,
  `docs/`). `.gitea/` and `.env` are not excluded.

## Compose (`docker-compose.yml`)

| Key | Value |
| --- | --- |
| Service / `container_name` | `Steam-Workshop-Notes` |
| Image | `ghcr.io/soulofsorrow/steam-patchnotes:latest`, with `build: .` |
| Environment | `LANG`, `MOD_IDS`, `COLLECTION_IDS`, `DISCORD_WEBHOOK_URL`, `SLEEP_INTERVAL`, `LOG_LEVEL`, `REQUESTS_TIMEOUT`, `SEND_ON_INSTALL`, `SEND_ON_STARTUP` from `.env` |
| Volume | `./config.json:/app/config.json` |
| Restart | `always` |

## CI

Job order: the check jobs (`lint`) run first. The image job `build-and-push` has `needs: [lint]` and starts only when all of them pass; on pull requests it builds without pushing.

Emulation: `docker/setup-qemu-action` is pinned to `tonistiigi/binfmt:qemu-v9.2.2`; with `latest` (QEMU 10) Node crashed with `Illegal instruction` in the arm64 build and the job hung. Job `build-and-push` has `timeout-minutes: 45`.

| File | Trigger | Jobs |
| --- | --- | --- |
| `.gitea/workflows/ci.yml` | push `main`, tags `v*.*.*`, PR to `main` | `ruff check .`, `compileall`; multi-arch image (`linux/amd64,linux/arm64`) to `${vars.REGISTRY_GITEA}` or `gitea.groot.rocks` via dind |
| `.github/workflows/ci.yml` | same | same checks; image to `ghcr.io` |
| `.github/workflows/release.yml` | tags `v*.*.*` | GitHub release via `softprops/action-gh-release` |

Image tags: branch, `pr-<n>`, semver `{{version}}` and `{{major}}.{{minor}}`,
`sha-<short>`, `latest` on the default branch.

## Release

No local release tooling. Pushing a `v*.*.*` tag builds versioned images and
(on GitHub) creates a release.
