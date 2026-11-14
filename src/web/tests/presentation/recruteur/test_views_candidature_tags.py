from unittest.mock import patch
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.recruteur.errors.tag_errors import TagOrganismeMismatch
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.tag.models import (
    CandidatureTagModel,
    CandidatureTagQuerySet,
    TagCategory,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
    create_recrutement_with_candidature,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    TagDjangoFactory,
)


def _candidature_tags_url(organisme_id, recrutement_id, candidature_id) -> str:
    return reverse(
        "recruteur:candidature_tags",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
        },
    )


class TestCandidatureTagsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _candidature_tags_url(uuid4(), uuid4(), uuid4())

        response = api_client.post(url, data={"tag_uuid": str(uuid4())}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CandidatureTagModel.objects.exists()

    def test_contributeur_is_forbidden(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(
                role=AgentOrganismeRole.AGENT, utilisateur=test_user
            )
        )
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=agent,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CandidatureTagModel.objects.exists()

    def test_requires_tag_uuid(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "tag_uuid" in response.json()

    def test_candidature_of_another_recrutement_is_not_found(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, _ = create_recrutement_and_candidature_for_agent(
            utilisateur=test_user
        )
        _, autre_candidature = create_recrutement_with_candidature(organisme)
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, autre_candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not CandidatureTagModel.objects.exists()

    def test_tag_of_another_organisme_is_not_found(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        tag = TagDjangoFactory(category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not CandidatureTagModel.objects.exists()

    def test_tag_of_another_category_is_rejected(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "tag_uuid" in response.json()
        assert not CandidatureTagModel.objects.exists()

    def test_tag_already_on_candidature_is_a_conflict(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        tag = CandidatureTagDjangoFactory(candidature=candidature).tag

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert (
            CandidatureTagModel.objects.filter(candidature=candidature, tag=tag).count()
            == 1
        )

    def test_tag_outside_the_candidature_organisme_is_not_found(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)
        erreur = TagOrganismeMismatch(tag.id, "candidature")

        # unreachable through the service, forced on the queryset
        with patch.object(CandidatureTagQuerySet, "poser", side_effect=erreur):
            response = authenticated_client.post(
                _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
                data={"tag_uuid": str(tag.id)},
                format="json",
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": str(erreur)}

    @pytest.mark.parametrize(
        ("organisme_role", "recrutement_role"),
        [
            (AgentOrganismeRole.SUPERVISEUR, None),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR),
        ],
        ids=["superviseur", "agent_responsable", "agent_recruteur"],
    )
    def test_tags_the_candidature(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(
                role=organisme_role, utilisateur=test_user
            )
        )
        if recrutement_role is not None:
            RecrutementAgentDjangoFactory(
                recrutement=recrutement, agent=agent, role=recrutement_role.value
            )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _candidature_tags_url(organisme.id, recrutement.pk, candidature.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.content == b""
        assert list(
            CandidatureTagModel.objects.filter(candidature=candidature).values_list(
                "tag_id", flat=True
            )
        ) == [tag.id]
