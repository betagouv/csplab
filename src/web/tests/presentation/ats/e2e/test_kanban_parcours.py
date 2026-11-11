import pytest
from playwright.sync_api import Locator, Page, expect

from tests.presentation.ats.e2e.locators import kanban_column


def kanban_card(page: Page, candidat: str) -> Locator:
    return page.get_by_role("article").filter(
        has=page.get_by_role("link", name=candidat)
    )


@pytest.fixture
def kanban(sign_in, recrutement_url) -> Page:
    page = sign_in("Marie")
    page.goto(recrutement_url)
    reception = kanban_column(page, "Réception des candidatures")
    expect(reception.get_by_role("link", name="Alice Martin")).to_be_visible()
    return page


@pytest.mark.e2e
class TestKanbanParcours:
    def test_etape_changed_from_the_panel_survives_a_reload(self, kanban: Page) -> None:
        kanban_url = kanban.url
        kanban.get_by_role("link", name="Alice Martin").click()
        panel = kanban.get_by_role("dialog", name="Alice Martin")
        panel.get_by_role("button", name="Changer d'étape").click()
        choice = kanban.get_by_role("dialog", name="Changer d'étape")
        choice.get_by_role("radio", name="Entretien").click()
        choice.get_by_role("button", name="Valider").click()
        expect(kanban.get_by_role("alert")).to_contain_text(
            "est passée à l'étape Entretien"
        )

        kanban.goto(kanban_url)

        entretien = kanban_column(kanban, "Entretien")
        expect(entretien.get_by_role("link", name="Alice Martin")).to_be_visible()

    def test_card_dropped_on_a_column_survives_a_reload(self, kanban: Page) -> None:
        preselection = kanban_column(kanban, "Présélection")
        kanban_card(kanban, "Lucas Fontaine").drag_to(preselection)
        expect(kanban.get_by_role("alert")).to_contain_text(
            "est passée à l'étape Présélection"
        )

        kanban.reload()

        expect(preselection.get_by_role("link", name="Lucas Fontaine")).to_be_visible()
