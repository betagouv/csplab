# Accessibility Testing

Automated accessibility tests using [pytest-playwright](https://playwright.dev/python/docs/test-runners) and [axe-playwright-python](https://pypi.org/project/axe-playwright-python/).

## Setup

```bash
make playwright-install                                  # First time only
```

## Usage

```bash
make test ARGS="-m accessibility --no-cov"               # Run a11y tests
make test ARGS="-m accessibility --headed --no-cov"      # Run with visible browser
make test ARGS="-m accessibility --slowmo 500 --no-cov"  # Run with slow-motion
```

## How it works

- **pytest-playwright** provides `page`, `context`, and `browser` fixtures automatically
- **axe-playwright-python** runs [axe-core](https://github.com/dequelabs/axe-core) accessibility checks on the rendered page
- **pytest-django** `live_server` fixture spins up a real Django server for Playwright to hit
- Tests are marked with `@pytest.mark.accessibility` so they can be run selectively
