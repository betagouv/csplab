# Environment variables

How configuration (environment variables and secrets) is loaded in dev and in production, via Scaleway Secret Manager. For the mise tooling side (tasks, `_.file`, `_.source`), see also [`docs/mise.md`](./mise.md#environnement).

## Overview

Each service (`web`, `ocr`, `ingestion`) combines two sources, layered in this order:

1. **`env.d/{service}`**: a local, gitignored file (copied from `env.d/{service}-example` by `mise run setup`), for non-secret, machine-specific values (local URLs, debug flags, etc.).
2. **Scaleway Secret Manager**: the actual secrets (API keys, passwords, tokens), fetched dynamically when mise computes the environment or when the process starts, and which **complement** the `env.d` file without ever overriding it.

This is the same mechanism in dev, in CI, and in production (Scalingo) — only how the Scaleway credentials are supplied changes.

```mermaid
flowchart TD
    subgraph Local["env.d/{service}"]
        EnvFile["Local, gitignored file\n(URLs, flags, non-secret values)"]
    end

    subgraph SM["Scaleway Secret Manager"]
        Secrets["/{service}/{SCALEWAY_ENV}\ne.g. /web/dev, /web/prod"]
    end

    EnvFile --> Merge["Process environment"]
    Secrets -->|"scaleway_secrets.fetch\n(skipped if already set by hand)"| Merge

    Merge --> App["Service (web / ocr / ingestion)"]
```

## In development

Each sub-project's `mise.toml` declares, in its `[env]` section:

```toml
[env]
_.file = "../../env.d/web"
_.python.venv = { path = ".venv" }
_.source = { path = "bin/inject_scaleway_env.sh", tools = true }
```

- `_.file` loads `env.d/web` (local values).
- `_.source` runs `bin/inject_scaleway_env.sh`, which queries Scaleway Secret Manager and exports whatever secrets are still missing.

`mise activate` recomputes this environment on every directory change: a mise task, or `mise en src/web` (sub-shell), always has the full configuration available, secrets included.

Prerequisite, once per machine: `scw init` (credentials stored in `~/.config/scw/config.yaml`), then set `SCALEWAY_ENV=dev` in `env.d/web` (already present in `env.d/web-example`). `mise run secrets:check` verifies access and lists the secret names available for each service, without printing their values.

Without `SCALEWAY_ENV` set, `bin/inject_scaleway_env.sh` is a no-op: the service runs with `env.d/{service}` alone.

> `notebook` is the exception: it has no `bin/inject_scaleway_env.sh` and no Scaleway secrets — its third-party credentials (Légifrance, Albert, OpenRouter, TalentSoft…) live in plain text directly in `env.d/notebook` (gitignored).

## The `inject_scaleway_env.sh` script

Each service has its own `bin/inject_scaleway_env.sh` (identical in principle for `web`, `ocr`, `ingestion`). It's meant to be *sourced*, not executed, so the exported variables persist in the calling shell:

```bash
source "$(dirname "$0")/inject_scaleway_env.sh"
```

It delegates the actual fetch to `libs/scaleway_secrets` (`python -m scaleway_secrets.fetch <service>`), which:

- lists every secret under `/{service}/{SCALEWAY_ENV}` in Scaleway Secret Manager;
- for each secret, if a variable of the same name is **already set** in the environment (e.g. set by hand on Scalingo), it's left untouched — Secret Manager never overrides it;
- otherwise, prints `export NAME=value`, which the bash script evaluates (`eval`).

Scaleway credentials come from the `scw` config file (`scw init`) in dev, or from the `SCW_ACCESS_KEY` / `SCW_SECRET_KEY` / `SCW_DEFAULT_PROJECT_ID` / `SCW_DEFAULT_REGION` environment variables in production (they take precedence over the config file when both exist).

A safety check prevents accidental misuse: `SCALEWAY_ENV=prod` is only allowed when `SCALINGO_APPLICATION_ID` is set, i.e. only on the Scalingo infrastructure.

## In production (Scalingo)

Application hosting (web, workers, deployment) runs on **Scalingo**; secrets themselves stay centralized in **Scaleway Secret Manager** — Scalingo is only the runtime.

Each `Procfile` sources the script before starting a process:

```
# src/web/Procfile
web: bash ./bin/start.sh
worker: bash ./bin/run_worker.sh
postdeploy: bash ./bin/postdeploy.sh
```

```bash
# bin/start.sh (excerpt)
source "$(dirname "${BASH_SOURCE[0]}")/inject_scaleway_env.sh"
...
gunicorn config.wsgi:application --log-file -
```

On Scalingo, `SCALEWAY_ENV=prod` and the `SCW_*` credentials are set once as application environment variables; at the start of each process (`web`, `worker`, `postdeploy`), the script fetches every secret under `/{service}/prod` before launching the actual command.

Deployment itself doesn't use the Scaleway API: the GitHub Actions CI (`.github/workflows/web.yml`, `ocr.yml`, `ingestion.yml`) simply pushes the `main` branch to a Scalingo deploy branch (`git push`, via the `.github/actions/scalingo-deploy` action), which triggers the build/deploy on Scalingo's side.

```mermaid
sequenceDiagram
    participant CI as GitHub Actions
    participant Scalingo
    participant Process as Process (web/worker/postdeploy)
    participant SM as Scaleway Secret Manager

    CI->>Scalingo: git push HEAD:main-web (deploy)
    Scalingo->>Process: start the process (Procfile)
    Process->>Process: source inject_scaleway_env.sh
    Process->>SM: fetch secrets under /web/prod
    SM-->>Process: export NAME=value (if not already set)
    Process->>Process: start the app (gunicorn / uvicorn / celery)
```

## Tests and CI

Test tasks load `env.test` (fake, versioned values, no network dependency) instead of `env.d/{service}`:

```toml
[tasks.test]
env = { _.file = "env.test" }
```

`mise.ci.toml`, layered on top of `mise.toml` in CI (`MISE_ENV=ci`), loads the same `env.test` and even disables the `scaleway-cli` tool (`disable_tools = ["scaleway-cli"]`). CI therefore never contacts Scaleway Secret Manager — which is why `inject_scaleway_env.sh` stays a no-op as long as `SCALEWAY_ENV` isn't set.

The root `mise.toml` also declares `redactions` (`*SECRET*`, `*_KEY`, `*PASSWORD*`, `*TOKEN*`, `*CREDENTIALS*`, `*DATABASE_URL*`) that mask these values in mise's logs/output, Scaleway secrets included.

## Adding or changing a secret

1. Create/update the secret in Scaleway Secret Manager, under `/{service}/{env}` (`dev`, `prod`…), with a secret name matching the expected variable name (case-insensitive — `fetch.py` uppercases it).
2. In dev: restart a mise shell (or `mise en src/web`) to reload the environment; verify with `mise run secrets:check`.
3. In production: nothing to redeploy — the secret is re-read the next time the process starts on Scalingo (manual restart or next deploy).

## Secrets backup to Vaultwarden

Demo and prod secrets only live in Scaleway Secret Manager. To keep a copy the team can read if the Scaleway project is lost, a developer copies them by hand into the incubator's Vaultwarden, one secure note per service and env, named `/{service}/{env}` (e.g. `/web/prod`), whose content is a list of `NAME=value` lines sorted by name.

The `export_secrets_vaultwarden` command of `web` prints what to paste:

```bash
scalingo --app csplab-web run bash
python manage.py export_secrets_vaultwarden
# or, in one step:
scalingo --app csplab-web run python manage.py export_secrets_vaultwarden
```

- It reads `SCALEWAY_ENV` and refuses anything other than `demo` or `prod`.
- It reads every secret under `/web/{env}`, `/ocr/{env}` and `/ingestion/{env}` with the app's `SCW_*` credentials, which must be allowed to read the three paths. If one of the three paths returns no secret (missing rights, wrong project, typo), the command stops with an error instead of printing an empty note that would overwrite a valid backup.
- For each note to update, it prints the added, removed and changed names, then the full note content to paste in place of the old one. Notes without changes are listed as up to date, without their content.
- The state of the last export lives in the Django cache (Redis), under `secrets_export:{env}`, without expiry: the date of the last run and, for each secret name, an HMAC-SHA256 of its value keyed with `SECRET_KEY`. No value is stored in clear, and reading Redis does not allow brute-forcing a weak secret.
- When every note is up to date, nothing is written: the printed date is the one of the last update of the notes.
- Otherwise, the state of every note is saved only after answering `o` to « Toutes les notes à mettre à jour ont été recopiées dans Vaultwarden ? [o/N] »: the answer covers all the printed notes. Answering anything else, or losing the session, keeps the previous state: the next run prints the same diff. If the state is lost (cache cleared, eviction), every note is printed again.

Values are printed in clear in the one-off container's terminal: run it from a trusted machine, and clear the terminal scrollback afterwards. Never run it with `scalingo run --detached`: a detached one-off's output goes to the application logs. Scalingo also records the input and output of one-off containers in the dashboard's Activity tab ([doc](https://doc.scalingo.com/platform/app/tasks)), so the printed values are readable there by the app's collaborators.

## Key files

| File | Role |
|---|---|
| `env.d/{service}-example` | Versioned template, copied by `mise run setup` |
| `env.d/{service}` | Local, gitignored file, non-secret values |
| `src/{service}/mise.toml` (`[env]`) | Declares `_.file` and `_.source` to load env.d + secrets |
| `src/{service}/bin/inject_scaleway_env.sh` | Script sourced by mise and by the Procfiles, no-op without `SCALEWAY_ENV` |
| `libs/scaleway_secrets/fetch.py` | Queries the Scaleway Secret Manager API, prints `export` lines |
| `src/web/application/commons/services/export_secrets_vaultwarden.py` | Reads the demo or prod secrets, computes which Vaultwarden notes to update, keeps the export state in Redis |
| `src/{service}/env.test` | Fake values for tests / CI |
| `src/{service}/Procfile` | Scalingo commands (web, worker, postdeploy) |
