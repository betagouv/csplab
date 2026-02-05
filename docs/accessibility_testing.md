# Accessibility Testing

Automated accessibility tests using [Playwright](https://playwright.dev/python/) and [axe-core](https://github.com/paciellogroup/axe-playwright-python).

## Usage

```bash
make playwright-install                                  # First time only
make test ARGS="-m accessibility"                        # Run tests
```

To run with visible browser, add to `env.d/tycho`:
```bash
TYCHO_HEADLESS_FUNCTIONAL_TESTS=False
```

Then run:
```bash
make test ARGS="-m accessibility"
```
