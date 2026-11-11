import re

from playwright.sync_api import Locator, Page


def notifications(page: Page) -> Locator:
    return page.get_by_role("region", name=re.compile("^Notifications"))


def kanban_column(page: Page, etape: str) -> Locator:
    title = page.get_by_role(
        "heading",
        level=2,
        name=re.compile(f"^Sélectionner la colonne {re.escape(etape)} "),
    )
    return page.locator("section").filter(has=title)
