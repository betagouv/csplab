from unittest.mock import patch

import pytest
from django.core.management import call_command
from referentiel.value_objects.source_type import SourceType

from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.users.models import UserModel

_CMD_MODULE = "presentation.identite.management.commands.create_user_with_source"
PASSWORD = "mot-de-passe-solide"  # noqa: S105


@pytest.fixture
def mock_getpass():
    with patch(f"{_CMD_MODULE}.getpass", return_value=PASSWORD) as mock:
        yield mock


def _mock_input(*answers: str):
    return patch("builtins.input", side_effect=list(answers))


@pytest.mark.django_db
class TestCreateUserWithSourceCommand:
    def test_creates_new_source_without_option(self, mock_getpass):
        with _mock_input("Jeanne", "Dupont", "Jeanne@Example.fr", "nouvelle-source"):
            call_command("create_user_with_source")

        user = UserModel.objects.get(email="jeanne@example.fr")
        source = SourceModel.objects.get(slug="nouvelle-source")
        assert source.type == SourceType.API.value
        assert list(user.sources.all()) == [source]
        assert user.check_password(PASSWORD)

    def test_attaches_existing_source_after_confirmation(self, mock_getpass):
        source = SourceModel.objects.create(
            slug="source-existante", type=SourceType.API.value
        )

        with _mock_input(
            "Jeanne", "Dupont", "jeanne@example.fr", "source-existante", "o"
        ):
            call_command("create_user_with_source")

        user = UserModel.objects.get(email="jeanne@example.fr")
        assert list(user.sources.all()) == [source]
        assert SourceModel.objects.count() == 1

    def test_asks_another_slug_when_existing_source_is_declined(self, mock_getpass):
        SourceModel.objects.create(slug="source-existante", type=SourceType.API.value)

        with _mock_input(
            "Jeanne",
            "Dupont",
            "jeanne@example.fr",
            "source-existante",
            "n",
            "nouvelle-source",
        ):
            call_command("create_user_with_source")

        user = UserModel.objects.get(email="jeanne@example.fr")
        assert list(user.sources.values_list("slug", flat=True)) == ["nouvelle-source"]

    def test_asks_another_slug_when_slug_is_ambiguous(self, mock_getpass):
        SourceModel.objects.create(slug="doublon", type=SourceType.API.value)
        SourceModel.objects.create(slug="doublon", type=SourceType.API.value)

        with _mock_input(
            "Jeanne", "Dupont", "jeanne@example.fr", "doublon", "nouvelle-source"
        ):
            call_command("create_user_with_source")

        user = UserModel.objects.get(email="jeanne@example.fr")
        assert list(user.sources.values_list("slug", flat=True)) == ["nouvelle-source"]
