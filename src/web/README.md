# Web - The CSPLab core server

This service is the first implementation of the future CSP suite developped by
the DGAFP.

## How-to

### Running Django management commands

Django management commands can be run using the `bin/manage` shortcut script
that will execute the well-kown `python manage.py` command in the `web`
service container wrapped with `uv`, _e.g._:

```sh
bin/manage makemigrations
```

is equivalent to:

```sh
docker compose run --rm web uv run python manage.py makemigrations
```

### Frontend Vue.js (ATS)

Le service web inclut un frontend Vue.js pour l'ATS (Applicant Tracking System).

```bash
make frontend-install   # Installer les dépendances
make frontend-dev       # Lancer Vite dev server (HMR)
make frontend-build     # Build production
```

Documentation : [docs/frontend_vue.md](../../docs/frontend_vue.md)

## License

This work is released under the MIT License (see LICENSE).
