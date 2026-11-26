import pytest
from playwright.sync_api import Page, expect

from tests.presentation.ats.e2e.locators import kanban_column
from tests.presentation.ats.seed import CANDIDAT_NAME


@pytest.fixture
def kanban(sign_in, recrutement_url) -> Page:
    page = sign_in("Marie")
    page.goto(recrutement_url)
    reception_column = kanban_column(page, "Réception des candidatures")
    expect(reception_column.get_by_role("link", name=CANDIDAT_NAME)).to_be_visible()
    return page
