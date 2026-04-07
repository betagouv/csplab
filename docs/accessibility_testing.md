# Accessibility Testing

Automated accessibility tests using [pytest-playwright](https://playwright.dev/python/docs/test-runners) and [axe-playwright-python](https://pypi.org/project/axe-playwright-python/).

## Setup

```bash
make playwright-install                                  # First time only
```

## Usage

```bash
make test-a11y                                           # Run a11y tests
make test-a11y ARGS="--headed"                           # Run with visible browser
make test-a11y ARGS="--slowmo 500"                       # Run with slow-motion
```

## How it works

- **pytest-playwright** provides `page`, `context`, and `browser` fixtures automatically
- **axe-playwright-python** runs [axe-core](https://github.com/dequelabs/axe-core) accessibility checks on the rendered page
- **pytest-django** `live_server` fixture spins up a real Django server for Playwright to hit
- Tests are marked with `@pytest.mark.accessibility` so they can be run selectively
