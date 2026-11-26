from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

WCAG_A_AND_AA = {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]}
EVERY_RULE_BUT_CONTRAST = {
    "runOnly": WCAG_A_AND_AA,
    "rules": {"color-contrast": {"enabled": False}},
    "resultTypes": ["violations"],
}
CONTRAST = {
    "runOnly": {"type": "rule", "values": ["color-contrast"]},
    "resultTypes": ["violations"],
}
# WCAG 1.4.3 exempts the text of an inactive component. axe misses the exemption
# when the text sits in a span of the label that wraps the disabled control.
ACTIVE_COMPONENTS = {"exclude": [["label:has(:disabled)"]]}


def assert_no_axe_violations(page: Page) -> None:
    axe = Axe()
    everywhere = axe.run(page, options=EVERY_RULE_BUT_CONTRAST)
    contrast = axe.run(page, context=ACTIVE_COMPONENTS, options=CONTRAST)
    violations = [*everywhere.response["violations"], *contrast.response["violations"]]
    assert violations == [], f"axe found {len(violations)} violation(s):\n" + "\n".join(
        f"- [{violation['id']}] {violation['help']}: {violation['nodes'][0]['html']}"
        for violation in violations
    )
