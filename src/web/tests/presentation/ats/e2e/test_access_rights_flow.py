import re

import pytest
from playwright.sync_api import Locator, Page, expect

from tests.presentation.ats.e2e.locators import notifications
from tests.presentation.ats.seed import AGENT_EMAILS, AGENT_NAMES, BRIANCON_NAME


def table_row(page: Page, email: str) -> Locator:
    return page.get_by_role("row").filter(has_text=email)


def search_agent(drawer: Locator, label: str, email: str) -> None:
    drawer.get_by_role("searchbox", name=label).fill(email)
    drawer.get_by_role("searchbox", name=label).press("Enter")
    expect(drawer.get_by_text(email)).to_be_visible()


def open_row_action(page: Page, name: str, action: str) -> None:
    page.get_by_role("button", name=f"Actions pour {name}").click()
    page.get_by_role("menuitem", name=action).click()


@pytest.mark.e2e
class TestAccessRightsFlow:
    def test_superviseur_manages_the_recrutement_team(
        self, sign_in, recrutement_url
    ) -> None:
        claire = AGENT_EMAILS["Claire"]
        page = sign_in("Marie")
        page.goto(f"{recrutement_url}/equipe")

        page.get_by_role("button", name="Ajouter un membre").click()
        drawer = page.get_by_role("dialog", name="Ajouter un membre")
        search_agent(drawer, "Courriel de l'agent", claire)
        drawer.get_by_role("radio", name="Contributeur").check()
        drawer.get_by_role("button", name="Ajouter le membre").click()
        expect(notifications(page)).to_contain_text("Membre ajouté")

        page.reload()
        expect(
            table_row(page, claire).get_by_role("cell", name="Contributeur", exact=True)
        ).to_be_visible()

        open_row_action(page, AGENT_NAMES["Claire"], "Modifier les droits d'accès")
        drawer = page.get_by_role("dialog", name="Modifier les droits d'accès")
        drawer.get_by_role("radio", name="Recruteur").check()
        drawer.get_by_role("button", name="Enregistrer les modifications").click()
        expect(notifications(page)).to_contain_text("Rôle modifié")

        page.reload()
        expect(
            table_row(page, claire).get_by_role("cell", name="Recruteur", exact=True)
        ).to_be_visible()

        open_row_action(page, AGENT_NAMES["Claire"], "Retirer de l'équipe")
        dialog = page.get_by_role("dialog", name="Retirer de l’équipe")
        dialog.get_by_role("button", name="Retirer de l’équipe").click()
        expect(notifications(page)).to_contain_text("Membre retiré")

        page.reload()
        expect(table_row(page, AGENT_EMAILS["Paul"])).to_be_visible()
        expect(table_row(page, claire)).to_have_count(0)

    def test_recruteur_cannot_open_the_recrutement_team(
        self, sign_in, recrutement_url
    ) -> None:
        page = sign_in("Paul")
        page.goto(recrutement_url)
        tabs = page.get_by_role("tablist")
        expect(tabs.get_by_role("tab", name="Candidatures")).to_be_visible()
        expect(tabs.get_by_role("tab", name="Équipe de recrutement")).to_have_count(0)

        page.goto(f"{recrutement_url}/equipe")

        expect(page.get_by_role("heading", level=1)).to_have_text("Accès refusé")
        expect(page.get_by_role("button", name="Ajouter un membre")).to_have_count(0)
        expect(page.get_by_role("table")).to_have_count(0)

    def test_superviseur_attaches_an_agent_and_changes_its_role(
        self, sign_in, organisme_url
    ) -> None:
        david = AGENT_EMAILS["David"]
        page = sign_in("Marie")
        page.goto(organisme_url)

        page.get_by_role("button", name="Ajouter un utilisateur").click()
        drawer = page.get_by_role("dialog", name="Ajouter un utilisateur")
        search_agent(drawer, "Courriel", david)
        drawer.get_by_role("radio", name="Agent").check()
        drawer.get_by_role("button", name="Ajouter l'utilisateur").click()
        expect(notifications(page)).to_contain_text("Utilisateur ajouté")

        page.reload()
        expect(
            table_row(page, david).get_by_role("cell", name="Agent", exact=True)
        ).to_be_visible()

        open_row_action(page, AGENT_NAMES["David"], "Modifier les droits d'accès")
        drawer = page.get_by_role("dialog", name="Modifier les droits d'accès")
        drawer.get_by_role("radio", name="Superviseur").check()
        drawer.get_by_role("button", name="Enregistrer les modifications").click()
        expect(notifications(page)).to_contain_text("Rôle modifié")

        page.reload()
        expect(
            table_row(page, david).get_by_role("cell", name="Superviseur", exact=True)
        ).to_be_visible()

    def test_settings_follow_the_role_in_the_selected_organisme(
        self, sign_in, organisme_url
    ) -> None:
        page = sign_in("Marc")
        page.goto(f"{organisme_url}/accueil")
        sidebar = page.get_by_role("complementary")
        settings_link = sidebar.get_by_role("link", name="Paramètres de l'organisme")
        expect(page.get_by_role("heading", level=1)).to_have_text("Bonjour Marc")
        expect(settings_link).to_have_count(0)

        sidebar.get_by_role("button", name=re.compile("Changer d'organisme")).click()
        page.get_by_role("option", name=BRIANCON_NAME).click()

        expect(
            sidebar.get_by_role(
                "button", name=re.compile(f"^Organisme : {re.escape(BRIANCON_NAME)}")
            )
        ).to_be_visible()
        settings_link.click()
        expect(page.get_by_role("tab", name="Comptes utilisateurs")).to_be_visible()

        page.goto(organisme_url)
        expect(page.get_by_role("heading", level=1)).to_have_text("Accès refusé")

    def test_agent_without_organisme_lands_on_an_empty_navigation(
        self, sign_in, live_server
    ) -> None:
        page = sign_in("David")
        page.goto(f"{live_server.url}/ats/")

        expect(
            page.get_by_text("Vous n’êtes rattaché à aucun organisme")
        ).to_be_visible()
        sidebar = page.get_by_role("complementary")
        expect(sidebar.get_by_role("button", name=AGENT_NAMES["David"])).to_be_visible()
        expect(sidebar.get_by_role("link")).to_have_count(0)
        expect(page).to_have_url(f"{live_server.url}/ats/")
