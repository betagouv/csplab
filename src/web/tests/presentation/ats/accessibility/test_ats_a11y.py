import re
from typing import Literal

import pytest
from playwright.sync_api import Locator, Page, expect

from tests.presentation.ats.seed import CANDIDAT_NAME
from tests.utils.axe import assert_no_axe_violations

LOADING = re.compile("^Chargement")

ReadyContent = Literal["button", "heading", "link", "table", "text"]


def content(page: Page, role: ReadyContent, name: str | re.Pattern) -> Locator:
    if role == "text":
        return page.get_by_text(name)
    return page.get_by_role(role, name=name)


def open_page(page: Page, url: str, role: ReadyContent, name: str | re.Pattern) -> None:
    page.goto(url)
    expect(content(page, role, name)).to_be_visible()
    expect(page.get_by_role("status", name=LOADING)).to_have_count(0)
    expect(page.locator(".csp-skeleton")).to_have_count(0)


def open_kanban(page: Page, recrutement_url: str) -> None:
    open_page(page, recrutement_url, "link", CANDIDAT_NAME)


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
        self,
        superviseur_page: Page,
        organisme_url: str,
        path: str,
        role: ReadyContent,
        name: str | re.Pattern,
    ) -> None:
        open_page(superviseur_page, organisme_url + path, role, name)

        assert_no_axe_violations(superviseur_page)

    @pytest.mark.parametrize(
        ("path", "role", "name"),
        [
            ("", "link", CANDIDAT_NAME),
            ("/liste", "table", "Candidatures"),
            ("/activites", "text", "Activités et tâches (à venir)"),
            ("/equipe", "table", "Équipe de recrutement"),
            ("/etapes-recrutement", "button", "Ajouter une étape"),
        ],
    )
    def test_recrutement_page_has_no_axe_violation(
        self,
        superviseur_page: Page,
        recrutement_url: str,
        path: str,
        role: ReadyContent,
        name: str | re.Pattern,
    ) -> None:
        open_page(superviseur_page, recrutement_url + path, role, name)

        assert_no_axe_violations(superviseur_page)

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
        self,
        superviseur_page: Page,
        candidature_url: str,
        path: str,
        role: ReadyContent,
        name: str | re.Pattern,
    ) -> None:
        open_page(superviseur_page, candidature_url + path, role, name)
        panel = superviseur_page.get_by_role("dialog", name=CANDIDAT_NAME)
        expect(panel).to_be_visible()

        assert_no_axe_violations(superviseur_page)

    def test_etape_change_dialog_has_no_axe_violation(
        self, superviseur_page: Page, candidature_url: str
    ) -> None:
        open_page(superviseur_page, candidature_url, "heading", "Curriculum vitae")
        superviseur_page.get_by_role("button", name="Changer d'étape").click()
        expect(
            superviseur_page.get_by_role("dialog", name="Changer d'étape")
        ).to_be_visible()

        assert_no_axe_violations(superviseur_page)

    def test_selected_kanban_column_has_no_axe_violation(
        self, superviseur_page: Page, recrutement_url: str
    ) -> None:
        select_reception_column(superviseur_page, recrutement_url)

        assert_no_axe_violations(superviseur_page)

    def test_rejection_dialog_has_no_axe_violation(
        self, superviseur_page: Page, recrutement_url: str
    ) -> None:
        select_reception_column(superviseur_page, recrutement_url)
        superviseur_page.get_by_role("button", name="Refuser").click()
        expect(
            superviseur_page.get_by_role("dialog", name="Refus de candidature")
        ).to_be_visible()

        assert_no_axe_violations(superviseur_page)
