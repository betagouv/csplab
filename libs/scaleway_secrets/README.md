# scaleway_secrets

Fetches every secret under `/{service}/{SCALEWAY_ENV}` in Scaleway Secret
Manager and prints `export NAME=value` lines, meant to be eval'd by a shell
script before a service's process starts.

Invoked as `python -m scaleway_secrets.fetch <service>` from each service's
`bin/inject_scaleway_env.sh`.

Credentials come from the `scw` config file (`scw init`, or `SCW_CONFIG_PATH`)
when it exists, and from the `SCW_*` env vars, which take precedence.

`--names` prints the secret names only, for diagnostics (`mise run secrets:check`).
