from datetime import UTC, datetime
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.tag.models import RecrutementAgentTagModel, TagCategory
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    RecrutementAgentTagDjangoFactory,
    TagDjangoFactory,
)


def _member_tags_url(organisme_id, recrutement_id, agent_id) -> str:
    return reverse(
        "recruteur:recrutement_agent_tags",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "agent_uuid": str(agent_id),
        },
    )


def _member_tag_url(organisme_id, recrutement_id, agent_id, tag_id) -> str:
    return reverse(
        "recruteur:recrutement_agent_tag",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "agent_uuid": str(agent_id),
            "tag_uuid": str(tag_id),
        },
    )


def _member_events(agent_id) -> list[str]:
    return list(
        AuditLogModel.objects.filter(
            ressource_kind="RecrutementAgent", ressource_id=agent_id
        ).values_list("event_name", flat=True)
    )


def _equipe(utilisateur, organisme_role, recrutement_role=None, **membre_kwargs):
    agent, organisme = create_organisme_with_agent(
        role=organisme_role, utilisateur=utilisateur
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    if recrutement_role is not None:
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, agent=agent, role=recrutement_role.value
        )
    membre = RecrutementAgentDjangoFactory(recrutement=recrutement, **membre_kwargs)
    return organisme, recrutement, membre


def _member_tag(organisme):
    return TagDjangoFactory(organisme=organisme, category=TagCategory.RECRUTEMENT_AGENT)


ROLES_AUTORISES = pytest.mark.parametrize(
    ("organisme_role", "recrutement_role"),
    [
        (AgentOrganismeRole.SUPERVISEUR, None),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
    ],
    ids=["superviseur", "agent_responsable"],
)

ROLES_REFUSES = pytest.mark.parametrize(
    "recrutement_role",
    [AgentRecrutementRole.CONTRIBUTEUR, AgentRecrutementRole.RECRUTEUR],
    ids=["contributeur", "recruteur"],
)


class TestRecrutementAgentTagsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _member_tags_url(uuid4(), uuid4(), uuid4())

        response = api_client.post(url, data={"tag_uuid": str(uuid4())}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @ROLES_REFUSES
    def test_member_without_responsable_role_is_forbidden(
        self, authenticated_client, test_user, recrutement_role
    ):
        organisme, recrutement, membre = _equipe(
            test_user, AgentOrganismeRole.AGENT, recrutement_role
        )
        tag = _member_tag(organisme)

        response = authenticated_client.post(
            _member_tags_url(organisme.id, recrutement.pk, membre.agent_id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not RecrutementAgentTagModel.objects.exists()
        assert _member_events(membre.agent_id) == []

    def test_revoked_member_is_not_found(self, authenticated_client, test_user):
        organisme, recrutement, membre = _equipe(
            test_user,
            AgentOrganismeRole.SUPERVISEUR,
            date_revocation=datetime.now(UTC),
        )
        tag = _member_tag(organisme)

        response = authenticated_client.post(
            _member_tags_url(organisme.id, recrutement.pk, membre.agent_id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not RecrutementAgentTagModel.objects.exists()
        assert _member_events(membre.agent_id) == []

    def test_tag_of_another_organisme_is_not_found(
        self, authenticated_client, test_user
    ):
        organisme, recrutement, membre = _equipe(
            test_user, AgentOrganismeRole.SUPERVISEUR
        )
        tag = TagDjangoFactory(category=TagCategory.RECRUTEMENT_AGENT)

        response = authenticated_client.post(
            _member_tags_url(organisme.id, recrutement.pk, membre.agent_id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not RecrutementAgentTagModel.objects.exists()
        assert _member_events(membre.agent_id) == []

    def test_tag_of_another_category_is_rejected(self, authenticated_client, test_user):
        organisme, recrutement, membre = _equipe(
            test_user, AgentOrganismeRole.SUPERVISEUR
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _member_tags_url(organisme.id, recrutement.pk, membre.agent_id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "tag_uuid" in response.json()
        assert not RecrutementAgentTagModel.objects.exists()
        assert _member_events(membre.agent_id) == []

    def test_member_already_tagged_is_a_conflict(self, authenticated_client, test_user):
        organisme, recrutement, membre = _equipe(
            test_user, AgentOrganismeRole.SUPERVISEUR
        )
        pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)

        response = authenticated_client.post(
            _member_tags_url(organisme.id, recrutement.pk, membre.agent_id),
            data={"tag_uuid": str(_member_tag(organisme).id)},
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert list(
            RecrutementAgentTagModel.objects.filter(
                recrutement_agent=membre
            ).values_list("pk", flat=True)
        ) == [pose.pk]
        assert _member_events(membre.agent_id) == []

    @ROLES_AUTORISES
    def test_tags_the_member(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        organisme, recrutement, membre = _equipe(
            test_user, organisme_role, recrutement_role
        )
        tag = _member_tag(organisme)

        response = authenticated_client.post(
            _member_tags_url(organisme.id, recrutement.pk, membre.agent_id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.content == b""
        assert list(
            RecrutementAgentTagModel.objects.filter(
                recrutement_agent=membre
            ).values_list("tag_id", flat=True)
        ) == [tag.id]
        assert _member_events(membre.agent_id) == ["EtiquettePosee"]


class TestRecrutementAgentTagDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _member_tag_url(uuid4(), uuid4(), uuid4(), uuid4())

        response = api_client.delete(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @ROLES_REFUSES
    def test_member_without_responsable_role_is_forbidden(
        self, authenticated_client, test_user, recrutement_role
    ):
        organisme, recrutement, membre = _equipe(
            test_user, AgentOrganismeRole.AGENT, recrutement_role
        )
        pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)

        response = authenticated_client.delete(
            _member_tag_url(organisme.id, recrutement.pk, membre.agent_id, pose.tag_id),
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert RecrutementAgentTagModel.objects.filter(pk=pose.pk).exists()
        assert _member_events(membre.agent_id) == []

    def test_revoked_member_is_not_found(self, authenticated_client, test_user):
        organisme, recrutement, membre = _equipe(
            test_user,
            AgentOrganismeRole.SUPERVISEUR,
            date_revocation=datetime.now(UTC),
        )
        pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)

        response = authenticated_client.delete(
            _member_tag_url(organisme.id, recrutement.pk, membre.agent_id, pose.tag_id),
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert RecrutementAgentTagModel.objects.filter(pk=pose.pk).exists()
        assert _member_events(membre.agent_id) == []

    def test_tag_not_on_member_is_not_found(self, authenticated_client, test_user):
        organisme, recrutement, membre = _equipe(
            test_user, AgentOrganismeRole.SUPERVISEUR
        )
        pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)
        autre = _member_tag(organisme)

        response = authenticated_client.delete(
            _member_tag_url(organisme.id, recrutement.pk, membre.agent_id, autre.id),
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "error": f"L'étiquette {autre.id} n'est pas posée sur ce membre"
        }
        assert RecrutementAgentTagModel.objects.filter(pk=pose.pk).exists()
        assert _member_events(membre.agent_id) == []

    @ROLES_AUTORISES
    def test_removes_only_this_member_tag(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        organisme, recrutement, membre = _equipe(
            test_user, organisme_role, recrutement_role
        )
        pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)
        autre_membre_pose = RecrutementAgentTagDjangoFactory(
            recrutement_agent__recrutement=recrutement, tag=pose.tag
        )

        response = authenticated_client.delete(
            _member_tag_url(organisme.id, recrutement.pk, membre.agent_id, pose.tag_id),
            format="json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert list(RecrutementAgentTagModel.objects.values_list("pk", flat=True)) == [
            autre_membre_pose.pk
        ]
        assert _member_events(membre.agent_id) == ["EtiquetteRetiree"]
