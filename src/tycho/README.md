# Tycho - The CSPLab Monolith

This service is the first implementation of the future CSP suite developped by
the DGAFP.

## How-to

### Running Django management commands

Django management commands can be run using the `bin/manage` shortcut script
that will execute the well-kown `python manage.py` command in the `tycho`
service container wrapped with `uv`, _e.g._:

```sh
bin/manage makemigrations
```

is equivalent to:

```sh
docker compose run --rm tycho uv run python manage.py makemigrations
```

## License

This work is released under the MIT License (see LICENSE).
