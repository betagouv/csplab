import re

import pytest
from django.conf import settings as django_settings
from playwright.sync_api import BrowserContext, Page, expect

from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


@pytest.mark.e2e
class TestAtsSmoke:
    def test_login_form_then_spa_boots(
        self, page: Page, live_server, agent_user: UserModel
    ) -> None:
        page.goto(f"{live_server.url}/utilisateur/connexion")
        page.get_by_label("Email").fill(agent_user.email)
        page.get_by_role("textbox", name="Mot de passe").fill(DEFAULT_PASSWORD)
        page.get_by_role("button", name="Se connecter").click()

        page.goto(f"{live_server.url}/ats/")
        expect(page.get_by_test_id("sidebar-user-info")).to_have_text(
            f"{agent_user.first_name} {agent_user.last_name}"
        )

    def test_session_cookie_authenticates_the_spa(
        self, authenticated_page: Page, live_server, agent_user: UserModel
    ) -> None:
        authenticated_page.goto(f"{live_server.url}/ats/")
        expect(authenticated_page.get_by_test_id("sidebar-user-info")).to_have_text(
            f"{agent_user.first_name} {agent_user.last_name}"
        )

    def test_login_form_rejects_bad_credentials(
        self, page: Page, live_server, agent_user: UserModel
    ) -> None:
        page.goto(f"{live_server.url}/utilisateur/connexion")
        page.get_by_label("Email").fill(agent_user.email)
        page.get_by_role("textbox", name="Mot de passe").fill("wrong-password")
        page.get_by_role("button", name="Se connecter").click()

        expect(page.get_by_role("alert")).to_contain_text(
            "Adresse e-mail ou mot de passe incorrect"
        )
        expect(page).to_have_url(re.compile("/utilisateur/connexion"))

    def test_invalid_session_redirects_to_login(
        self, page: Page, context: BrowserContext, live_server, db
    ) -> None:
        context.add_cookies(
            [
                {
                    "name": django_settings.SESSION_COOKIE_NAME,
                    "value": "invalid-session",
                    "url": live_server.url,
                }
            ]
        )
        page.goto(f"{live_server.url}/ats/")

        expect(page).to_have_url(
            re.compile(r"/utilisateur/connexion\?next="), timeout=10000
        )
