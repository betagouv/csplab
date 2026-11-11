import pytest
from playwright.sync_api import Page, expect

from tests.presentation.ats.e2e.locators import kanban_column, notifications
from tests.presentation.ats.seed import CANDIDAT_NAME, CANDIDAT_NAMES


@pytest.mark.e2e
class TestRejectionFlow:
    def test_reception_column_refused_in_batch_survives_a_reload(
        self, kanban: Page
    ) -> None:
        reception_column = kanban_column(kanban, "Réception des candidatures")

        kanban.get_by_role(
            "checkbox", name="Sélectionner la colonne Réception des candidatures"
        ).click()
        kanban.get_by_role("button", name="Refuser").click()
        dialog = kanban.get_by_role("dialog", name="Refus de candidature")
        dialog.get_by_role("combobox", name="Motif de refus").click()
        kanban.get_by_role("option", name="Expérience insuffisante").click()
        dialog.get_by_role("button", name="Valider le refus").click()
        expect(notifications(kanban)).to_contain_text(
            "2 candidatures sont passées à l'étape Refus"
        )

        kanban.reload()

        rejected_column = kanban_column(kanban, "Refus")
        expect(rejected_column.get_by_role("link", name=CANDIDAT_NAME)).to_be_visible()
        expect(
            rejected_column.get_by_role("link", name=CANDIDAT_NAMES["Lucas"])
        ).to_be_visible()
        expect(reception_column.get_by_role("article")).to_have_count(0)

        rejected_column.get_by_role("link", name=CANDIDAT_NAME).click()
        panel = kanban.get_by_role("dialog", name=CANDIDAT_NAME)
        expect(panel.get_by_role("region", name="Motif de refus")).to_contain_text(
            "Expérience insuffisante"
        )
