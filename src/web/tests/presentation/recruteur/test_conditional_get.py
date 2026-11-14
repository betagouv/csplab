from uuid import uuid4

import pytest
from django.urls import URLPattern, get_resolver, reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from presentation.commons.conditional_get import ConditionalGetMixin


@pytest.fixture(name="recrutement")
def recrutement_fixture(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    return RecrutementDjangoFactory(organisme=organisme)


def _detail_url(recrutement) -> str:
    return reverse(
        "recruteur:organisme_recrutement",
        kwargs={
            "organisme_uuid": recrutement.organisme_id,
            "recrutement_uuid": recrutement.pk,
        },
    )


@pytest.mark.django_db
class TestConditionalGet:
    def test_response_carries_etag_and_private_no_cache(
        self, authenticated_client, recrutement
    ):
        response = authenticated_client.get(_detail_url(recrutement))

        assert response.status_code == status.HTTP_200_OK
        assert response["ETag"]
        assert set(response["Cache-Control"].split(", ")) == {"private", "no-cache"}

    def test_returns_304_when_nothing_changed(self, authenticated_client, recrutement):
        first = authenticated_client.get(_detail_url(recrutement))

        second = authenticated_client.get(
            _detail_url(recrutement), HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_304_NOT_MODIFIED
        assert second.content == b""
        assert second["ETag"] == first["ETag"]
        assert set(second["Cache-Control"].split(", ")) == {"private", "no-cache"}

    def test_returns_200_after_a_change_by_someone_else(
        self, authenticated_client, recrutement
    ):
        first = authenticated_client.get(_detail_url(recrutement))
        recrutement.offre.title = "Nouvel intitulé"
        recrutement.offre.save()

        second = authenticated_client.get(
            _detail_url(recrutement), HTTP_IF_NONE_MATCH=first["ETag"]
        )

        assert second.status_code == status.HTTP_200_OK
        assert second.json()["intitule"] == "Nouvel intitulé"
        assert second["ETag"] != first["ETag"]

    def test_error_responses_have_no_etag(self, authenticated_client, recrutement):
        url = reverse(
            "recruteur:organisme_recrutement",
            kwargs={
                "organisme_uuid": recrutement.organisme_id,
                "recrutement_uuid": uuid4(),
            },
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not response.has_header("ETag")


def test_every_recruteur_view_supports_conditional_get():
    patterns = get_resolver().url_patterns
    [recruteur] = [p for p in patterns if getattr(p, "namespace", None) == "recruteur"]
    views = [
        p.callback.view_class
        for p in recruteur.url_patterns
        if isinstance(p, URLPattern)
    ]

    assert views
    assert [v for v in views if not issubclass(v, ConditionalGetMixin)] == []
