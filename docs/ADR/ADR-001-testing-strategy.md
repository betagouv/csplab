
# ADR-001: Testing Strategy

**Status:** Accepted
**Date:** 2026.03.12
**Deciders:** Élodie R, Lucas P, Vincent P
**Tags:** testing

---

## Context

Need to harmonize testing practices

---

## Decision Drivers

- Be confident that critical components are battle-tested
- Test each behavior once — avoid duplication across layers
- Use coverage as a lighthouse
- Consider accessibility and keyboard navigation controls
- Cover main end-to-end user stories
- Keep tests and CI pipeline fast
- Minimize the effort required to update tests when the codebase evolves
- Do not test what we are not responsible for (third-party libraries, external APIs)
- Keep the test suite codebase lean and maintainable
- Ensure tests are repeatable and representative of real usage
- Isolate the impact of third-party libraries on test stability
- Clearly distinguish what must block a PR from what is informational

---

## Considered Options

1. **Option A** — All tests managed by pytest
2. **Option B** — All tests managed by Playwright
3. **Option C** — The test suite runs all tests on every execution
4. **Option D** — Balanced test suite with non-blocking warning tests

---

## Decision Outcome

**Chosen option: Option D**, because it assigns the right tool to the right layer,
avoids test duplication, keeps CI fast, and maintains high confidence on critical paths
without over-engineering lower-risk areas.

### Ground Rules

**Test data**
- External gateways are never tested directly — they are always mocked
- Python fixtures are reused across tests to produce coherent, consistent datasets, even in e2e and a11y tests
- JSON fixtures are loaded to seed subset data repositories (e.g. ROME referential)

**Blocking tests** — these must pass for a PR to be merged:
- Repository methods are tested exhaustively, including all edge cases, with **pytest**
- Use cases are tested including conditionals and error handling (excluding repository
  errors already covered), with **pytest**
- Main end-to-end user stories (those executed by ~80% of users) are tested with
  **Playwright**

**Non-blocking tests** — these run but do not gate merges:
- Accessibility and keyboard navigation tests are run at the start of each sprint
  iteration, results are tracked but do not block PRs

### Positive Consequences

- Regressions on critical paths are caught early in CI
- Each behavior is tested exactly once, reducing redundancy and maintenance cost
- The test suite stays fast enough to run on every PR
- External dependencies cannot cause flaky test failures
- Accessibility debt is tracked without slowing down daily delivery

### Negative Consequences / Trade-offs

- Developers must understand which layer owns which test, requiring onboarding effort
- Mocking external gateways means integration failures with third parties can go
  undetected until staging or production. Failure with third parties will be check with healthcheck services
- Non-blocking accessibility tests may accumulate unaddressed issues if not reviewed
  consistently each sprint

---

## Pros and Cons of the Options

### Option A — All tests with pytest

**Description:** Every test — unit, integration, e2e, and accessibility — is written
and run using pytest. Playwright or browser-based tooling is not introduced.

- ✅ Single tool, low cognitive overhead for the team
- ✅ Consistent test authoring patterns across the codebase
- ❌ pytest is not designed for browser-based e2e or accessibility testing
- ❌ Simulating real user journeys in a browser requires heavy workarounds
- ❌ Accessibility checks (WCAG, keyboard nav) are impractical without a real DOM

---

### Option B — All tests with Playwright

**Description:** Every test — including unit and repository tests — is written using
Playwright. Python backend logic is tested through the UI layer.

- ✅ Tests reflect real user experience end-to-end
- ✅ Native accessibility and keyboard navigation support
- ❌ Playwright tests are slow — running all tests on every PR is not viable
- ❌ Repository and use case logic is only tested indirectly, making debugging hard
- ❌ High cost to maintain browser tests for low-level business logic edge cases

---

### Option C — Full test suite on every run

**Description:** No test selection or tiering — every test (unit, integration, e2e,
accessibility) runs on every CI trigger regardless of what changed.

- ✅ Maximum coverage confidence on every push
- ✅ No risk of skipping a relevant test
- ❌ CI execution time becomes prohibitive as the suite grows
- ❌ Flaky or slow accessibility tests block all PRs indiscriminately
- ❌ Developers reduce test coverage to keep CI manageable — opposite of the goal

---

### Option D — Balanced suite with non-blocking tests ✅ Chosen

**Description:** Tests are split by layer and assigned to the right tool. Blocking tests
(pytest for repositories and use cases, Playwright for critical e2e paths) gate PR
merges. Non-blocking tests (accessibility, keyboard navigation) run on a sprint cadence
without blocking daily delivery.

- ✅ Each layer is tested with the most appropriate tool
- ✅ CI stays fast — only relevant, blocking tests run on every PR
- ✅ Accessibility is tracked without becoming a daily bottleneck
- ✅ Clear ownership: developers know exactly what to write and where
- ❌ Requires discipline to respect layer boundaries and avoid test duplication
- ❌ Non-blocking tests need active sprint review, or findings accumulate silently

---

## Implementation Notes

- [ ] Add tests to check that in-memory repository respect interfaces
- [ ] Audit existing use case tests and strip out any assertions that duplicate
      repository-level coverage
- [ ] Identify the top 80% user stories and ensure each has a Playwright e2e test
- [ ] Set up accessibility and keyboard navigation tests in Playwright; mark them
      as non-blocking in CI configuration
- [ ] Document the factory and fixture conventions so all team members produce
      consistent test data
- [ ] Add a test layer guide to the project README or contributing guide
