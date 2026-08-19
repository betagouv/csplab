from pathlib import Path

import pytest
from django.conf import settings as django_settings
from django.test import Client
from playwright.sync_api import BrowserContext, Page

from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.seed_recruteur_datas import seed_recruteur_datas

SEED_AGENT_EMAIL = "marie.dupont@transition-eco.gouv.fr"


@pytest.fixture(scope="session", autouse=True)
def require_frontend_build() -> None:
    manifest = Path(django_settings.STATIC_DIR) / "frontend" / "manifest.json"
    if not manifest.exists():
        pytest.fail(
            "Frontend build missing: the ATS e2e tests serve the built SPA. "
            "Run `make frontend-build` first."
        )


@pytest.fixture(autouse=True)
def insecure_cookies(settings) -> None:
    # live_server serves plain http; Secure cookies would never reach it.
    settings.SESSION_COOKIE_SECURE = False
    settings.CSRF_COOKIE_SECURE = False


@pytest.fixture
def seed(db) -> dict:
    return seed_recruteur_datas(force=True)


@pytest.fixture
def agent_user(seed) -> UserModel:
    return UserModel.objects.get(email=SEED_AGENT_EMAIL)


@pytest.fixture
def authenticated_page(
    page: Page, context: BrowserContext, live_server, agent_user
) -> Page:
    client = Client()
    client.force_login(agent_user)
    session_cookie = client.cookies[django_settings.SESSION_COOKIE_NAME]
    context.add_cookies(
        [
            {
                "name": django_settings.SESSION_COOKIE_NAME,
                "value": session_cookie.value,
                "url": live_server.url,
            }
        ]
    )
    return page
