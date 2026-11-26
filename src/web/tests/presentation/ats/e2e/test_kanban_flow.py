import pytest
from playwright.sync_api import Locator, Page, expect

from tests.presentation.ats.e2e.locators import kanban_column, notifications
from tests.presentation.ats.seed import CANDIDAT_NAME, CANDIDAT_NAMES


def kanban_card(page: Page, candidat: str) -> Locator:
    return page.get_by_role("article").filter(
        has=page.get_by_role("link", name=candidat)
    )


@pytest.mark.e2e
class TestKanbanFlow:
    def test_etape_changed_from_the_panel_survives_a_reload(self, kanban: Page) -> None:
        kanban_url = kanban.url
        kanban.get_by_role("link", name=CANDIDAT_NAME).click()
        panel = kanban.get_by_role("dialog", name=CANDIDAT_NAME)
        panel.get_by_role("button", name="Changer d'étape").click()
        choice = kanban.get_by_role("dialog", name="Changer d'étape")
        choice.get_by_role("radio", name="Entretien").click()
        choice.get_by_role("button", name="Valider").click()
        expect(notifications(kanban)).to_contain_text("est passée à l'étape Entretien")

        kanban.goto(kanban_url)

        interview_column = kanban_column(kanban, "Entretien")
        expect(interview_column.get_by_role("link", name=CANDIDAT_NAME)).to_be_visible()

    def test_card_dropped_on_a_column_survives_a_reload(self, kanban: Page) -> None:
        shortlist_column = kanban_column(kanban, "Présélection")
        kanban_card(kanban, CANDIDAT_NAMES["Lucas"]).drag_to(shortlist_column)
        expect(notifications(kanban)).to_contain_text(
            "est passée à l'étape Présélection"
        )

        kanban.reload()

        expect(
            shortlist_column.get_by_role("link", name=CANDIDAT_NAMES["Lucas"])
        ).to_be_visible()
