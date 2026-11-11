import pytest
from playwright.sync_api import expect

from tests.presentation.ats.e2e.locators import kanban_column, notifications


@pytest.mark.e2e
class TestRefusParcours:
    def test_reception_column_refused_in_batch_survives_a_reload(
        self, sign_in, recrutement_url
    ) -> None:
        page = sign_in("Marie")
        page.goto(recrutement_url)
        reception = kanban_column(page, "Réception des candidatures")
        expect(reception.get_by_role("link", name="Alice Martin")).to_be_visible()

        page.get_by_role(
            "checkbox", name="Sélectionner la colonne Réception des candidatures"
        ).click()
        page.get_by_role("button", name="Refuser").click()
        dialog = page.get_by_role("dialog", name="Refus de candidature")
        dialog.get_by_role("combobox", name="Motif de refus").click()
        page.get_by_role("option", name="Expérience insuffisante").click()
        dialog.get_by_role("button", name="Valider le refus").click()
        expect(notifications(page)).to_contain_text(
            "2 candidatures sont passées à l'étape Refus"
        )

        page.reload()

        refus = kanban_column(page, "Refus")
        expect(refus.get_by_role("link", name="Alice Martin")).to_be_visible()
        expect(refus.get_by_role("link", name="Lucas Fontaine")).to_be_visible()
        expect(reception.get_by_role("article")).to_have_count(0)

        refus.get_by_role("link", name="Alice Martin").click()
        panel = page.get_by_role("dialog", name="Alice Martin")
        expect(panel.get_by_role("region", name="Motif de refus")).to_contain_text(
            "Expérience insuffisante"
        )
