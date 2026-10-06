from unittest.mock import patch
from uuid import uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from domain.candidate.exceptions.document_errors import FichierDeposeIncomplet
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import MessageModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    MessageDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from presentation.recruteur.views.candidature_conversation_detail import (
    MessagePagination,
)
from tests.utils.message_documents import INVALID_DOCUMENTS, valid_documents

TAILLE_PAGE_LIMITEE = 2
TAILLE_PAGE_PAR_DEFAUT = 20
NB_MESSAGES = 3


def _url(organisme_uuid, recrutement_uuid, candidature_uuid, conversation_uuid):
    return reverse(
        "recruteur:organisme_recrutement_candidature_conversation_detail",
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
    conversation = ConversationDjangoFactory(candidature=candidature)
    MessageDjangoFactory(conversation=conversation, with_document=True)
    MessageDjangoFactory.create_batch(NB_MESSAGES - 1, conversation=conversation)
    return conversation.pk


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


NOT_FOUND_CASES = [
    pytest.param(_unknown_organisme, id="unknown_organisme"),
    pytest.param(_unknown_recrutement, id="unknown_recrutement"),
    pytest.param(
        _recrutement_from_another_organisme, id="recrutement_from_another_organisme"
    ),
    pytest.param(
        _candidature_from_another_recrutement, id="candidature_from_another_recrutement"
    ),
    pytest.param(_unknown_candidature, id="unknown_candidature"),
    pytest.param(_unknown_conversation, id="unknown_conversation"),
    pytest.param(
        _conversation_from_another_candidature,
        id="conversation_from_another_candidature",
    ),
]


AUTHORIZED_ROLES = pytest.mark.parametrize(
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

HTTP_METHODS = pytest.mark.parametrize("method", ["get", "post"])


def _call(client, method, url):
    if method == "post":
        return client.post(url, {"content": "Bonjour"}, format="multipart")
    return client.get(url)


def _authorized_url(test_user, organisme_role, recrutement_role):
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
    return _url(
        organisme.id, recrutement.pk, candidature.pk, _conversation_of(candidature)
    )


def _superviseur_url(test_user):
    return _authorized_url(test_user, AgentOrganismeRole.SUPERVISEUR, None)


class TestCandidatureConversationDetailView:
    @HTTP_METHODS
    def test_anonymous_access_is_unauthorized(self, api_client, method):
        response = _call(api_client, method, _url(uuid4(), uuid4(), uuid4(), uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @HTTP_METHODS
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.AGENT, None], ids=["no_recrutement_role", "no_role"]
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role, method):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        recrutement, candidature = _candidature_for(organisme)

        response = _call(
            authenticated_client,
            method,
            _url(
                organisme.id,
                recrutement.pk,
                candidature.pk,
                _conversation_of(candidature),
            ),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @HTTP_METHODS
    @pytest.mark.parametrize("build_ids", NOT_FOUND_CASES)
    def test_returns_404_for(self, authenticated_client, test_user, build_ids, method):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement, candidature = _candidature_for(organisme)

        response = _call(
            authenticated_client,
            method,
            _url(*build_ids(organisme, recrutement, candidature)),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @AUTHORIZED_ROLES
    def test_authorized_agent_reads_conversation(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        response = authenticated_client.get(
            _authorized_url(test_user, organisme_role, recrutement_role)
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["count"] == NB_MESSAGES
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
        assert len(documents) == 1
        assert set(documents[0].keys()) == {
            "uuid",
            "nom",
            "type",
            "content_type",
            "taille",
        }

    def test_limit_param_caps_page_size(self, authenticated_client, test_user):
        response = authenticated_client.get(
            _superviseur_url(test_user), {"limit": TAILLE_PAGE_LIMITEE}
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert len(body["results"]) == TAILLE_PAGE_LIMITEE
        assert body["next"] is not None

    def test_out_of_range_page_returns_404(self, authenticated_client, test_user):
        response = authenticated_client.get(_superviseur_url(test_user), {"page": 999})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_default_page_size_is_20(self):
        assert MessagePagination.page_size == TAILLE_PAGE_PAR_DEFAUT

    @AUTHORIZED_ROLES
    def test_authorized_agent_replies(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        response = authenticated_client.post(
            _authorized_url(test_user, organisme_role, recrutement_role),
            {"content": "Merci", "documents": valid_documents()},
            format="multipart",
        )

        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()
        assert body["content"] == "Merci"
        assert body["author"] == f"{test_user.first_name} {test_user.last_name}"
        assert [document["nom"] for document in body["documents"]] == [
            "cv.pdf",
            "lettre.pdf",
            "diplome.pdf",
            "photo.png",
            "scan.jpg",
        ]
        assert all(document["uuid"] for document in body["documents"])

    def test_reply_is_persisted_audited_and_listed(
        self, authenticated_client, test_user
    ):
        url = _superviseur_url(test_user)

        created = authenticated_client.post(
            url,
            {"content": "Merci", "documents": valid_documents()},
            format="multipart",
        ).json()

        message = MessageModel.objects.get(contenu="Merci")
        assert message.auteur_id == test_user.username
        assert message.pieces_jointes.count() == len(created["documents"])

        audit = AuditLogModel.objects.get(ressource_id=message.pk)
        assert audit.ressource_kind == "Message"
        assert audit.event_name == "MessageCree"

        listed = authenticated_client.get(url).json()["results"]
        assert listed[-1]["content"] == "Merci"
        assert listed[-1]["created_at"] == created["created_at"]
        assert len(listed) == NB_MESSAGES + 1

    def test_incomplete_uploaded_file_is_a_bad_request(
        self, authenticated_client, test_user
    ):
        with patch(
            "presentation.recruteur.views.candidature_conversation_detail.reply_conversation",
            side_effect=FichierDeposeIncomplet(),
        ):
            response = authenticated_client.post(
                _superviseur_url(test_user),
                {"content": "Bonjour"},
                format="multipart",
            )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": str(FichierDeposeIncomplet())}

    def test_content_whitespace_is_preserved(self, authenticated_client, test_user):
        response = authenticated_client.post(
            _superviseur_url(test_user),
            {"content": "    code\n"},
            format="multipart",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["content"] == "    code\n"

    @pytest.mark.parametrize(
        "payload",
        [{}, {"content": ""}, {"content": " \n\t"}],
        ids=["missing_content", "blank_content", "whitespace_only_content"],
    )
    def test_invalid_content_is_rejected(
        self, authenticated_client, test_user, payload
    ):
        response = authenticated_client.post(
            _superviseur_url(test_user), payload, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "content" in response.json()

    @pytest.mark.parametrize("build_documents", INVALID_DOCUMENTS)
    def test_invalid_documents_are_rejected(
        self, authenticated_client, test_user, build_documents
    ):
        response = authenticated_client.post(
            _superviseur_url(test_user),
            {"content": "Bonjour", "documents": build_documents()},
            format="multipart",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "documents" in response.json()
