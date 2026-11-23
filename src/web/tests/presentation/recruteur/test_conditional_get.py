from uuid import uuid4

import pytest
from django.urls import URLResolver, get_resolver, reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from presentation.commons.conditional_get import ConditionalGetMixin, NoStoreMixin


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


def _view_classes(resolver: URLResolver):
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            yield from _view_classes(pattern)
        else:
            yield pattern.callback.view_class  # type: ignore[attr-defined]


def test_every_recruteur_get_view_sets_a_cache_policy():
    _, recruteur = get_resolver().namespace_dict["recruteur"]
    get_views = [view for view in _view_classes(recruteur) if hasattr(view, "get")]

    assert get_views
    assert [
        v
        for v in get_views
        if issubclass(v, ConditionalGetMixin) == issubclass(v, NoStoreMixin)
    ] == []
