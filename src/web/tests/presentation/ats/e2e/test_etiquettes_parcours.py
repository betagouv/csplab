import pytest
from playwright.sync_api import expect

from tests.presentation.ats.e2e.locators import notifications


@pytest.mark.e2e
class TestEtiquettesParcours:
    def test_superviseure_creates_renames_and_deletes_an_etiquette(
        self, sign_in, organisme_url
    ) -> None:
        page = sign_in("Marie")
        page.goto(f"{organisme_url}/etiquettes")
        candidature = page.get_by_role("region", name="Candidature", exact=True)

        candidature.get_by_role("button", name="Ajouter une étiquette").click()
        drawer = page.get_by_role("dialog", name="Ajouter une étiquette")
        drawer.get_by_role("textbox", name="Libellé").fill("À relancer")
        drawer.get_by_role("button", name="Enregistrer").click()
        expect(notifications(page)).to_contain_text("Étiquette ajoutée")

        page.reload()
        candidature.get_by_role(
            "button", name="Modifier l'étiquette À relancer"
        ).click()
        drawer = page.get_by_role("dialog", name="Modifier l'étiquette")
        drawer.get_by_role("textbox", name="Libellé").fill("Profil prioritaire")
        drawer.get_by_role("button", name="Enregistrer").click()
        expect(notifications(page)).to_contain_text("Étiquette modifiée")

        page.reload()
        renamed = candidature.get_by_role(
            "button", name="Modifier l'étiquette Profil prioritaire"
        )
        expect(renamed).to_be_visible()
        expect(
            candidature.get_by_role("button", name="Modifier l'étiquette À relancer")
        ).to_have_count(0)

        candidature.get_by_role(
            "button", name="Supprimer l'étiquette Profil prioritaire"
        ).click()
        dialog = page.get_by_role(
            "dialog", name="Supprimer l'étiquette « Profil prioritaire »"
        )
        dialog.get_by_role("button", name="Supprimer", exact=True).click()
        expect(notifications(page)).to_contain_text("Étiquette supprimée")

        page.reload()
        expect(candidature.get_by_text("Aucune étiquette.")).to_be_visible()
        expect(renamed).to_have_count(0)
