from collections.abc import Callable
from pathlib import Path

import pytest
from django.conf import settings as django_settings
from django.test import Client
from playwright.sync_api import BrowserContext, Page

from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.seed_recruteur_datas import (
    _AGENTS_SPECS,
    _ORGANISME_UUID,
    seed_recruteur_datas,
)

SEED_AGENT_EMAILS = {spec["prenom"]: spec["email"] for spec in _AGENTS_SPECS}


def add_session_cookie(context: BrowserContext, user: UserModel, url: str) -> None:
    client = Client()
    client.force_login(user)
    context.add_cookies(
        [
            {
                "name": django_settings.SESSION_COOKIE_NAME,
                "value": client.cookies[django_settings.SESSION_COOKIE_NAME].value,
                "url": url,
            }
        ]
    )


@pytest.fixture(scope="session")
def require_frontend_build() -> None:
    manifest = Path(django_settings.STATIC_DIR) / "frontend" / "manifest.json"
    if not manifest.exists():
        pytest.fail(
            "Frontend build missing: the ATS browser tests serve the built SPA. "
            "Run `mise front:build` first."
        )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {**browser_context_args, "locale": "fr-FR", "reduced_motion": "reduce"}


@pytest.fixture
def insecure_cookies(settings) -> None:
    # live_server serves plain http; Secure cookies would never reach it.
    settings.SESSION_COOKIE_SECURE = False
    settings.CSRF_COOKIE_SECURE = False


@pytest.fixture
def agent_user(db) -> UserModel:
    return AgentDjangoFactory.create().utilisateur


@pytest.fixture
def authenticated_page(
    page: Page,
    context: BrowserContext,
    live_server,
    agent_user,
    require_frontend_build,
    insecure_cookies,
) -> Page:
    add_session_cookie(context, agent_user, live_server.url)
    return page


@pytest.fixture
def seeded_recruteur(transactional_db) -> None:
    seed_recruteur_datas()


@pytest.fixture
def sign_in(
    new_context, live_server, seeded_recruteur, require_frontend_build, insecure_cookies
) -> Callable[[str], Page]:
    def open_page_as(prenom: str) -> Page:
        user = UserModel.objects.get(email=SEED_AGENT_EMAILS[prenom])
        context = new_context()
        add_session_cookie(context, user, live_server.url)
        return context.new_page()

    return open_page_as


@pytest.fixture
def organisme_url(live_server) -> str:
    return f"{live_server.url}/ats/organismes/{_ORGANISME_UUID}"
