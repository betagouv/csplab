# Browser Auto-Reload

Uses **django-browser-reload** to automatically reload the browser during development when templates, CSS, or Python files change.

## Usage

```bash
make dev
```

Starts Django server + Sass watch mode with auto-reload.

## Configuration

- [config/settings/dev.py](../src/tycho/config/settings/dev.py) - Django settings
- [config/urls.py](../src/tycho/config/urls.py) - `__reload__/` endpoint
- [Makefile](../../Makefile) - `dev` target runs both processes

## Details

- Only active in DEBUG mode
- Uses Server-Sent Events (no WebSocket)

## Resources

- [django-browser-reload](https://github.com/adamchainz/django-browser-reload)
