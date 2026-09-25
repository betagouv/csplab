from uuid import uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from application.recruteur.services.list_conversations import (
    _CONVERSATIONS,
    stub_conversation_id,
)
from application.recruteur.services.read_conversation import (
    _MESSAGES,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from presentation.recruteur.views.candidature_conversation_detail import (
    MessagePagination,
)

OBJET = _CONVERSATIONS[0][0]
TAILLE_PAGE_LIMITEE = 2
TAILLE_PAGE_PAR_DEFAUT = 20


def _url(organisme_uuid, recrutement_uuid, candidature_uuid, conversation_uuid):
    return reverse(
        "recruteur:organisme-recrutement-candidature-conversation-detail",
        kwargs={
            "organisme_uuid": organisme_uuid,
            "recrutement_uuid": recrutement_uuid,
            "candidature_uuid": candidature_uuid,
            "conversation_uuid": conversation_uuid,
        },
    )


def _candidature_for(organisme):
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    return recrutement, candidature


def _conversation_of(candidature):
    return stub_conversation_id(candidature.pk, OBJET)


def _unknown_organisme(organisme, recrutement, candidature):
    return uuid4(), recrutement.pk, candidature.pk, _conversation_of(candidature)


def _unknown_recrutement(organisme, recrutement, candidature):
    return organisme.id, uuid4(), candidature.pk, _conversation_of(candidature)


def _recrutement_from_another_organisme(organisme, recrutement, candidature):
    autre_recrutement = RecrutementDjangoFactory(organisme=OrganismeDjangoFactory())
    return (
        organisme.id,
        autre_recrutement.pk,
        candidature.pk,
        _conversation_of(candidature),
    )


def _candidature_from_another_recrutement(organisme, recrutement, candidature):
    _, autre_candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        autre_candidature.pk,
        _conversation_of(autre_candidature),
    )


def _unknown_candidature(organisme, recrutement, candidature):
    return organisme.id, recrutement.pk, uuid4(), _conversation_of(candidature)


def _unknown_conversation(organisme, recrutement, candidature):
    return organisme.id, recrutement.pk, candidature.pk, uuid4()


def _conversation_from_another_candidature(organisme, recrutement, candidature):
    autre_candidature = CandidatureDjangoFactory(etape=candidature.etape)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _conversation_of(autre_candidature),
    )


class TestCandidatureConversationDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(_url(uuid4(), uuid4(), uuid4(), uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "organisme_role,recrutement_role",
        [
            (AgentOrganismeRole.SUPERVISEUR, None),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR),
            (AgentOrganismeRole.AGENT, AgentRecrutementRole.CONTRIBUTEUR),
        ],
        ids=[
            "superviseur",
            "agent_responsable",
            "agent_recruteur",
            "agent_contributeur",
        ],
    )
    def test_authorized_agent_reads_conversation(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        _, organisme = create_organisme_with_agent(
            role=organisme_role, utilisateur=test_user
        )
        recrutement, candidature = _candidature_for(organisme)
        if recrutement_role is not None:
            RecrutementAgentDjangoFactory(
                recrutement=recrutement,
                agent=test_user.profil_agent,
                role=recrutement_role.value,
            )
        conversation_uuid = _conversation_of(candidature)

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.pk, conversation_uuid)
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["count"] == len(_MESSAGES)
        results = body["results"]
        assert set(results[0].keys()) == {
            "content",
            "author",
            "created_at",
            "documents",
        }
        dates = [message["created_at"] for message in results]
        assert dates == sorted(dates)
        assert all(
            len(message["documents"]) <= settings.MESSAGE_MAX_DOCUMENTS
            for message in results
        )
        documents = [doc for message in results for doc in message["documents"]]
        assert set(documents[0].keys()) == {
            "uuid",
            "nom",
            "type",
            "content_type",
            "taille",
        }

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.AGENT, None], ids=["no_recrutement_role", "no_role"]
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        recrutement, candidature = _candidature_for(organisme)

        response = authenticated_client.get(
            _url(
                organisme.id,
                recrutement.pk,
                candidature.pk,
                _conversation_of(candidature),
            )
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "build_ids",
        [
            _unknown_organisme,
            _unknown_recrutement,
            _recrutement_from_another_organisme,
            _candidature_from_another_recrutement,
            _unknown_candidature,
            _unknown_conversation,
            _conversation_from_another_candidature,
        ],
        ids=[
            "unknown_organisme",
            "unknown_recrutement",
            "recrutement_from_another_organisme",
            "candidature_from_another_recrutement",
            "unknown_candidature",
            "unknown_conversation",
            "conversation_from_another_candidature",
        ],
    )
    def test_returns_404_for(self, authenticated_client, test_user, build_ids):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement, candidature = _candidature_for(organisme)

        response = authenticated_client.get(
            _url(*build_ids(organisme, recrutement, candidature))
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_limit_param_caps_page_size(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement, candidature = _candidature_for(organisme)

        response = authenticated_client.get(
            _url(
                organisme.id,
                recrutement.pk,
                candidature.pk,
                _conversation_of(candidature),
            ),
            {"limit": TAILLE_PAGE_LIMITEE},
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert len(body["results"]) == TAILLE_PAGE_LIMITEE
        assert body["next"] is not None

    def test_out_of_range_page_returns_404(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement, candidature = _candidature_for(organisme)

        response = authenticated_client.get(
            _url(
                organisme.id,
                recrutement.pk,
                candidature.pk,
                _conversation_of(candidature),
            ),
            {"page": 999},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_default_page_size_is_20(self):
        assert MessagePagination.page_size == TAILLE_PAGE_PAR_DEFAUT
