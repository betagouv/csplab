# Accessibility Testing

Automated accessibility tests using [pytest-playwright](https://playwright.dev/python/docs/test-runners) and [axe-playwright-python](https://pypi.org/project/axe-playwright-python/).

## Setup

```bash
mise run web:install:playwright           # First time only
```

## Usage

```bash
mise run web:test:a11y                    # Run a11y tests
mise run web:test:a11y -- --headed        # Run with visible browser
mise run web:test:a11y -- --slowmo 500    # Run with slow-motion
```

## How it works

- **pytest-playwright** provides `page`, `context`, and `browser` fixtures automatically
- **axe-playwright-python** runs [axe-core](https://github.com/dequelabs/axe-core) accessibility checks on the rendered page
- **pytest-django** `live_server` fixture spins up a real Django server for Playwright to hit
- Tests are marked with `@pytest.mark.accessibility` so they can be run selectively

## ATS pages

`src/web/tests/presentation/ats/accessibility/` runs axe (WCAG 2.1 A and AA rules) on the pages of the ATS: organisme pages, recrutement pages, the tabs of the candidature panel, the étape change and refus dialogs. These tests block a PR ([ADR-001](./ADR/ADR-001-testing-strategy.md)).

```bash
mise run web:test:a11y -- tests/presentation/ats
```

- The task builds the frontend, and the tests serve it through `live_server`.
- `seeded_recruteur` loads the demo dataset and `sign_in("Marie")` opens a page signed in as that agent of the dataset (`tests/presentation/ats/conftest.py`).
- The browser asks for reduced motion, so a dialog is at full opacity when axe reads its contrast.
- `assert_no_axe_violations(page)` (`tests/utils/axe.py`) runs axe. Its contrast check leaves out the labels of disabled controls, which WCAG 1.4.3 exempts.
- When you add a page or a dialog to the ATS, add a case to `test_ats_a11y.py`.
