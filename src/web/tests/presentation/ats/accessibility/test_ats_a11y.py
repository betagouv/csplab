import re

import pytest
from playwright.sync_api import Locator, Page, expect

from tests.utils.axe import assert_no_axe_violations

LOADING = re.compile("^Chargement")


def content(page: Page, role: str, name: str | re.Pattern) -> Locator:
    if role == "text":
        return page.get_by_text(name)
    return page.get_by_role(role, name=name)  # type: ignore[arg-type]


def open_page(page: Page, url: str, role: str, name: str | re.Pattern) -> None:
    page.goto(url)
    expect(content(page, role, name)).to_be_visible()
    expect(page.get_by_role("status", name=LOADING)).to_have_count(0)
    expect(page.locator(".csp-skeleton")).to_have_count(0)


def open_kanban(page: Page, recrutement_url: str) -> None:
    open_page(page, recrutement_url, "link", "Alice Martin")


def select_reception_column(page: Page, recrutement_url: str) -> None:
    open_kanban(page, recrutement_url)
    page.get_by_role(
        "checkbox", name="Sélectionner la colonne Réception des candidatures"
    ).first.click()
    expect(page.get_by_role("button", name="Refuser")).to_be_visible()


@pytest.mark.accessibility
class TestAtsAccessibility:
    @pytest.mark.parametrize(
        ("path", "role", "name"),
        [
            ("/accueil", "heading", re.compile("^Prêt à démarrer")),
            ("/recrutements", "table", "Recrutements en cours"),
            ("/recrutements/archives", "table", "Recrutements terminés"),
            ("", "table", "Comptes utilisateurs de l'organisme"),
            ("/etapes", "button", "Ajouter une étape"),
            ("/etiquettes", "heading", "Candidature"),
        ],
    )
    def test_organisme_page_has_no_axe_violation(
        self, superviseure_page: Page, organisme_url: str, path: str, role: str, name
    ) -> None:
        open_page(superviseure_page, organisme_url + path, role, name)

        assert_no_axe_violations(superviseure_page)

    @pytest.mark.parametrize(
        ("path", "role", "name"),
        [
            ("", "link", "Alice Martin"),
            ("/liste", "table", "Candidatures"),
            ("/activites", "text", "Activités et tâches (à venir)"),
            ("/equipe", "table", "Équipe de recrutement"),
            ("/etapes-recrutement", "button", "Ajouter une étape"),
        ],
    )
    def test_recrutement_page_has_no_axe_violation(
        self, superviseure_page: Page, recrutement_url: str, path: str, role: str, name
    ) -> None:
        open_page(superviseure_page, recrutement_url + path, role, name)

        assert_no_axe_violations(superviseure_page)

    @pytest.mark.parametrize(
        ("path", "role", "name"),
        [
            ("", "heading", "Curriculum vitae"),
            ("/historique", "heading", re.compile("activités récentes$")),
            ("/documents", "heading", re.compile("^1 document")),
            ("/notes", "text", "Aucune note sur cette candidature"),
            ("/messages", "heading", "Conversation"),
            ("/messages/nouveau", "heading", "Créer une nouvelle conversation"),
        ],
    )
    def test_candidature_panel_has_no_axe_violation(
        self, superviseure_page: Page, candidature_url: str, path: str, role: str, name
    ) -> None:
        open_page(superviseure_page, candidature_url + path, role, name)
        panel = superviseure_page.get_by_role("dialog", name="Alice Martin")
        expect(panel).to_be_visible()

        assert_no_axe_violations(superviseure_page)

    def test_etape_change_dialog_has_no_axe_violation(
        self, superviseure_page: Page, candidature_url: str
    ) -> None:
        open_page(superviseure_page, candidature_url, "heading", "Curriculum vitae")
        superviseure_page.get_by_role("button", name="Changer d'étape").click()
        expect(
            superviseure_page.get_by_role("dialog", name="Changer d'étape")
        ).to_be_visible()

        assert_no_axe_violations(superviseure_page)

    def test_selected_kanban_column_has_no_axe_violation(
        self, superviseure_page: Page, recrutement_url: str
    ) -> None:
        select_reception_column(superviseure_page, recrutement_url)

        assert_no_axe_violations(superviseure_page)

    def test_refus_dialog_has_no_axe_violation(
        self, superviseure_page: Page, recrutement_url: str
    ) -> None:
        select_reception_column(superviseure_page, recrutement_url)
        superviseure_page.get_by_role("button", name="Refuser").click()
        expect(
            superviseure_page.get_by_role("dialog", name="Refus de candidature")
        ).to_be_visible()

        assert_no_axe_violations(superviseure_page)
