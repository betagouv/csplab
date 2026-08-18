import pytest
from playwright.sync_api import Page, expect

from tests.presentation.ats.e2e.conftest import SEED_AGENT_EMAIL


@pytest.mark.e2e
class TestAtsSmoke:
    def test_login_form_then_spa_boots(
        self, page: Page, live_server, seed: dict
    ) -> None:
        page.goto(f"{live_server.url}/utilisateur/connexion")
        page.get_by_label("Email").fill(SEED_AGENT_EMAIL)
        page.get_by_role("textbox", name="Mot de passe").fill(seed["seed_password"])
        page.get_by_role("button", name="Se connecter").click()

        page.goto(f"{live_server.url}/ats/")
        expect(page.get_by_test_id("sidebar-user-info")).to_have_text("Marie Dupont")

    def test_session_cookie_authenticates_the_spa(
        self, authenticated_page: Page, live_server
    ) -> None:
        authenticated_page.goto(f"{live_server.url}/ats/")
        expect(authenticated_page.get_by_test_id("sidebar-user-info")).to_have_text(
            "Marie Dupont"
        )
