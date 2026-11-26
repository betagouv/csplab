import pytest
from playwright.sync_api import Locator, Page, expect

from infrastructure.django_apps.tag.models import TagCategory
from infrastructure.factories.tag.tag_django_factory import TagDjangoFactory
from tests.presentation.ats.seed import CANDIDAT_NAME

TAG = "À rappeler"


@pytest.fixture
def candidature_tag(recrutement) -> None:
    TagDjangoFactory(
        organisme=recrutement.organisme, category=TagCategory.CANDIDATURE, name=TAG
    )


def candidature_tags(page: Page) -> Locator:
    panel = page.get_by_role("dialog", name=CANDIDAT_NAME)
    return panel.get_by_role("list", name="Étiquettes de la candidature")


@pytest.mark.e2e
class TestTagsFlow:
    def test_superviseur_tags_then_untags_a_candidature(
        self, kanban: Page, candidature_tag
    ) -> None:
        kanban.get_by_role("link", name=CANDIDAT_NAME).click()
        kanban.get_by_role(
            "button", name="Ajouter une étiquette à la candidature"
        ).click()
        picker = kanban.get_by_role(
            "dialog", name="Ajouter une étiquette à la candidature"
        )
        picker.get_by_role("button", name=f"Ajouter l'étiquette {TAG}").click()
        expect(candidature_tags(kanban)).to_contain_text(TAG)

        kanban.reload()
        expect(candidature_tags(kanban)).to_contain_text(TAG)

        kanban.get_by_role("button", name=f"Retirer l'étiquette {TAG}").click()
        expect(candidature_tags(kanban)).to_have_count(0)

        kanban.reload()
        expect(kanban.get_by_role("dialog", name=CANDIDAT_NAME)).to_be_visible()
        expect(candidature_tags(kanban)).to_have_count(0)
