import re

import pytest
from django.conf import settings as django_settings
from playwright.sync_api import BrowserContext, Page, expect

from infrastructure.django_apps.users.models import UserModel


@pytest.mark.e2e
class TestAtsSmoke:
    def test_session_cookie_authenticates_the_spa(
        self, authenticated_page: Page, live_server, agent_user: UserModel
    ) -> None:
        authenticated_page.goto(f"{live_server.url}/ats/")
        expect(
            authenticated_page.get_by_role(
                "button", name=f"{agent_user.first_name} {agent_user.last_name}"
            )
        ).to_be_visible()

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
