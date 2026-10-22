from datetime import UTC, datetime
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.tag.models import TagCategory, TagModel
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import TagDjangoFactory
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def _tags_url(organisme_id) -> str:
    return reverse(
        "recruteur:organisme_parametres_tags",
        kwargs={"organisme_uuid": str(organisme_id)},
    )


def _tag_url(organisme_id, tag_id) -> str:
    return reverse(
        "recruteur:organisme_parametres_tag",
        kwargs={"organisme_uuid": str(organisme_id), "tag_uuid": str(tag_id)},
    )


def _logs(tag_id):
    return PostgresAuditLogRepository().get_logs_for_ressource("Tag", tag_id)


@pytest.fixture(name="superviseur_organisme")
def superviseur_organisme_fixture(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
    )
    return organisme


@pytest.fixture(name="agent_organisme")
def agent_organisme_fixture(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    return organisme


@pytest.fixture(name="staff_client")
def staff_client_fixture(api_client):
    api_client.force_login(UtilisateurDjangoFactory(is_staff=True))
    return api_client


class TestListTags:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(_tags_url(uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_agent_of_another_organisme_is_forbidden(
        self, authenticated_client, agent_organisme
    ):
        _, other_organisme = create_organisme_with_agent()

        response = authenticated_client.get(_tags_url(other_organisme.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_revoked_agent_is_forbidden(
        self, authenticated_client, test_user, agent_organisme
    ):
        OrganismeAgentModel.objects.filter(
            organisme_id=agent_organisme.id, agent__utilisateur=test_user
        ).update(date_revocation=datetime.now(UTC))

        response = authenticated_client.get(_tags_url(agent_organisme.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unknown_organisme_is_not_found(self, authenticated_client):
        response = authenticated_client.get(_tags_url(uuid4()))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deleted_organisme_is_not_found(
        self, authenticated_client, superviseur_organisme
    ):
        TagDjangoFactory(organisme=superviseur_organisme)
        superviseur_organisme.supprime_le = datetime.now(UTC)
        superviseur_organisme.save(update_fields=["supprime_le"])

        response = authenticated_client.get(_tags_url(superviseur_organisme.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT]
    )
    def test_member_gets_organisme_tags_sorted_by_name_ignoring_case(
        self, authenticated_client, test_user, role
    ):
        _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        expert_note = TagDjangoFactory(
            organisme=organisme, name="expert", category=TagCategory.NOTE
        )
        expert_candidature = TagDjangoFactory(
            organisme=organisme, name="Expert", category=TagCategory.CANDIDATURE
        )
        bon_profil = TagDjangoFactory(
            organisme=organisme, name="Bon profil", category=TagCategory.NOTE
        )
        a_rappeler = TagDjangoFactory(
            organisme=organisme, name="À rappeler", category=TagCategory.CANDIDATURE
        )
        TagDjangoFactory(name="Autre organisme")

        response = authenticated_client.get(_tags_url(organisme.id))

        assert response.status_code == status.HTTP_200_OK
        assert [tag["uuid"] for tag in response.json()["results"]] == [
            str(a_rappeler.id),
            str(bon_profil.id),
            str(expert_candidature.id),
            str(expert_note.id),
        ]

    def test_staff_gets_organisme_tags(self, staff_client):
        _, organisme = create_organisme_with_agent()
        tag = TagDjangoFactory(organisme=organisme)

        response = staff_client.get(_tags_url(organisme.id))

        assert response.status_code == status.HTTP_200_OK
        assert [t["uuid"] for t in response.json()["results"]] == [str(tag.id)]

    def test_returns_tag_fields(self, authenticated_client, agent_organisme):
        tag = TagDjangoFactory(
            organisme=agent_organisme,
            name="Expert",
            category=TagCategory.RECRUTEMENT_AGENT,
            color="violet",
        )

        response = authenticated_client.get(_tags_url(agent_organisme.id))

        assert response.json()["results"] == [
            {
                "uuid": str(tag.id),
                "name": "Expert",
                "category": "recrutement_agent",
                "color": "violet",
            }
        ]

    def test_filters_by_category(self, authenticated_client, agent_organisme):
        note_tag = TagDjangoFactory(
            organisme=agent_organisme, category=TagCategory.NOTE
        )
        TagDjangoFactory(organisme=agent_organisme, category=TagCategory.CANDIDATURE)
        TagDjangoFactory(category=TagCategory.NOTE)

        response = authenticated_client.get(
            _tags_url(agent_organisme.id), {"category": "note"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert [t["uuid"] for t in response.json()["results"]] == [str(note_tag.id)]

    def test_unknown_category_is_a_bad_request(
        self, authenticated_client, agent_organisme
    ):
        response = authenticated_client.get(
            _tags_url(agent_organisme.id), {"category": "offre"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestCreateTag:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(
            _tags_url(uuid4()),
            data={"name": "Expert", "category": "candidature"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superviseur_creates_tag(self, authenticated_client, superviseur_organisme):
        response = authenticated_client.post(
            _tags_url(superviseur_organisme.id),
            data={"name": "Expert", "category": "note", "color": "rose"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        tag = TagModel.objects.get()
        assert response.json() == {
            "uuid": str(tag.id),
            "name": "Expert",
            "category": "note",
            "color": "rose",
        }
        assert tag.organisme_id == superviseur_organisme.id
        (log,) = _logs(tag.id)
        assert log.event_name == "TagCree"

    def test_color_defaults_to_bleu(self, authenticated_client, superviseur_organisme):
        response = authenticated_client.post(
            _tags_url(superviseur_organisme.id),
            data={"name": "Expert", "category": "candidature"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["color"] == "bleu"

    def test_agent_is_forbidden(self, authenticated_client, agent_organisme):
        response = authenticated_client.post(
            _tags_url(agent_organisme.id),
            data={"name": "Expert", "category": "candidature"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not TagModel.objects.exists()
        assert not AuditLogModel.objects.exists()

    def test_name_taken_in_category_ignoring_case_is_a_conflict(
        self, authenticated_client, superviseur_organisme
    ):
        existing = TagDjangoFactory(
            organisme=superviseur_organisme,
            name="Expert",
            category=TagCategory.CANDIDATURE,
        )

        response = authenticated_client.post(
            _tags_url(superviseur_organisme.id),
            data={"name": "EXPERT", "category": "candidature"},
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert list(TagModel.objects.all()) == [existing]
        assert not AuditLogModel.objects.exists()

    def test_name_taken_in_another_category_is_accepted(
        self, authenticated_client, superviseur_organisme
    ):
        TagDjangoFactory(
            organisme=superviseur_organisme,
            name="Expert",
            category=TagCategory.CANDIDATURE,
        )

        response = authenticated_client.post(
            _tags_url(superviseur_organisme.id),
            data={"name": "Expert", "category": "note"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "data",
        [
            {"category": "candidature"},
            {"name": "Expert"},
            {"name": "Expert", "category": "offre"},
            {"name": "Expert", "category": "candidature", "color": "#000091"},
        ],
        ids=["sans_nom", "sans_categorie", "categorie_inconnue", "couleur_hexa"],
    )
    def test_invalid_payload_is_a_bad_request(
        self, authenticated_client, superviseur_organisme, data
    ):
        response = authenticated_client.post(
            _tags_url(superviseur_organisme.id), data=data, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not TagModel.objects.exists()


class TestUpdateTag:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.put(
            _tag_url(uuid4(), uuid4()),
            data={"name": "Expert", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superviseur_updates_name_and_color(
        self, authenticated_client, superviseur_organisme
    ):
        tag = TagDjangoFactory(
            organisme=superviseur_organisme,
            name="Expert",
            category=TagCategory.NOTE,
            color="bleu",
        )

        response = authenticated_client.put(
            _tag_url(superviseur_organisme.id, tag.id),
            data={"name": "Profil expert", "color": "rose"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "uuid": str(tag.id),
            "name": "Profil expert",
            "category": "note",
            "color": "rose",
        }
        tag.refresh_from_db()
        assert (tag.name, tag.category, tag.color) == ("Profil expert", "note", "rose")
        (log,) = _logs(tag.id)
        assert log.event_name == "TagModifie"

    def test_changes_only_the_case_of_its_own_name(
        self, authenticated_client, superviseur_organisme
    ):
        tag = TagDjangoFactory(organisme=superviseur_organisme, name="expert")

        response = authenticated_client.put(
            _tag_url(superviseur_organisme.id, tag.id),
            data={"name": "Expert", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        tag.refresh_from_db()
        assert tag.name == "Expert"

    def test_name_taken_in_category_ignoring_case_is_a_conflict(
        self, authenticated_client, superviseur_organisme
    ):
        TagDjangoFactory(
            organisme=superviseur_organisme,
            name="Expert",
            category=TagCategory.CANDIDATURE,
        )
        tag = TagDjangoFactory(
            organisme=superviseur_organisme,
            name="Bon profil",
            category=TagCategory.CANDIDATURE,
        )

        response = authenticated_client.put(
            _tag_url(superviseur_organisme.id, tag.id),
            data={"name": "EXPERT", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        tag.refresh_from_db()
        assert tag.name == "Bon profil"
        assert not AuditLogModel.objects.exists()

    def test_agent_is_forbidden(self, authenticated_client, agent_organisme):
        tag = TagDjangoFactory(organisme=agent_organisme, name="Expert")

        response = authenticated_client.put(
            _tag_url(agent_organisme.id, tag.id),
            data={"name": "Bon profil", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        tag.refresh_from_db()
        assert tag.name == "Expert"
        assert not AuditLogModel.objects.exists()

    def test_staff_updates_tag(self, staff_client):
        _, organisme = create_organisme_with_agent()
        tag = TagDjangoFactory(organisme=organisme, name="Expert")

        response = staff_client.put(
            _tag_url(organisme.id, tag.id),
            data={"name": "Bon profil", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        tag.refresh_from_db()
        assert tag.name == "Bon profil"

    def test_tag_of_another_organisme_is_not_found(
        self, authenticated_client, superviseur_organisme
    ):
        other_tag = TagDjangoFactory(name="Expert")

        response = authenticated_client.put(
            _tag_url(superviseur_organisme.id, other_tag.id),
            data={"name": "Bon profil", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        other_tag.refresh_from_db()
        assert other_tag.name == "Expert"
        assert not AuditLogModel.objects.exists()

    def test_unknown_tag_is_not_found(
        self, authenticated_client, superviseur_organisme
    ):
        response = authenticated_client.put(
            _tag_url(superviseur_organisme.id, uuid4()),
            data={"name": "Bon profil", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unknown_organisme_is_not_found(self, authenticated_client):
        response = authenticated_client.put(
            _tag_url(uuid4(), uuid4()),
            data={"name": "Bon profil", "color": "bleu"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_hexadecimal_color_is_a_bad_request(
        self, authenticated_client, superviseur_organisme
    ):
        tag = TagDjangoFactory(organisme=superviseur_organisme, color="bleu")

        response = authenticated_client.put(
            _tag_url(superviseur_organisme.id, tag.id),
            data={"name": "Expert", "color": "#000091"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        tag.refresh_from_db()
        assert tag.color == "bleu"
