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
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageDocumentModel,
    MessageModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_with_candidature,
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
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from presentation.recruteur.views.candidature_conversations import (
    ConversationPagination,
)
from tests.utils.message_documents import INVALID_DOCUMENTS, valid_documents

TAILLE_PAGE_LIMITEE = 2
TAILLE_PAGE_PAR_DEFAUT = 20
NB_CONVERSATIONS = 2


def _url(organisme_uuid, recrutement_uuid, candidature_uuid):
    return reverse(
        "recruteur:organisme_recrutement_candidature_conversations",
        kwargs={
            "organisme_uuid": organisme_uuid,
            "recrutement_uuid": recrutement_uuid,
            "candidature_uuid": candidature_uuid,
        },
    )


def _conversation_with_messages(candidature, *contenus):
    conversation = ConversationDjangoFactory(candidature=candidature)
    for contenu in contenus:
        MessageDjangoFactory(conversation=conversation, contenu=contenu)
    return conversation


def _unknown_organisme(organisme, recrutement, candidature):
    return uuid4(), recrutement.pk, candidature.pk


def _unknown_recrutement(organisme, recrutement, candidature):
    return organisme.id, uuid4(), candidature.pk


def _recrutement_from_another_organisme(organisme, recrutement, candidature):
    autre_recrutement = RecrutementDjangoFactory(organisme=OrganismeDjangoFactory())
    return organisme.id, autre_recrutement.pk, candidature.pk


def _candidature_from_another_recrutement(organisme, recrutement, candidature):
    _, autre_candidature = create_recrutement_with_candidature(organisme)
    return organisme.id, recrutement.pk, autre_candidature.pk


def _unknown_candidature(organisme, recrutement, candidature):
    return organisme.id, recrutement.pk, uuid4()


def _payload(**overrides):
    return {"objet": "Convocation", "content": "Bonjour", **overrides}


AUTHORIZED_ROLES = pytest.mark.parametrize(
    "organisme_role,recrutement_role",
    [
        (AgentOrganismeRole.SUPERVISEUR, None),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.RESPONSABLE),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.RECRUTEUR),
        (AgentOrganismeRole.AGENT, AgentRecrutementRole.CONTRIBUTEUR),
    ],
    ids=["superviseur", "agent_responsable", "agent_recruteur", "agent_contributeur"],
)
BOTH_METHODS = pytest.mark.parametrize("method", ["get", "post"])
UNKNOWN_OR_FOREIGN_IDS = pytest.mark.parametrize(
    "build_ids",
    [
        _unknown_organisme,
        _unknown_recrutement,
        _recrutement_from_another_organisme,
        _candidature_from_another_recrutement,
        _unknown_candidature,
    ],
    ids=[
        "unknown_organisme",
        "unknown_recrutement",
        "recrutement_from_another_organisme",
        "candidature_from_another_recrutement",
        "unknown_candidature",
    ],
)


def _call(client, method, url, **payload):
    if method == "post":
        return client.post(url, _payload(**payload), format="multipart")
    return client.get(url)


def _grant(test_user, organisme_role, recrutement_role):
    agent, organisme = create_organisme_with_agent(
        role=organisme_role, utilisateur=test_user
    )
    recrutement, candidature = create_recrutement_with_candidature(organisme)
    if recrutement_role is not None:
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=test_user.profil_agent,
            role=recrutement_role.value,
        )
    return agent, organisme, recrutement, candidature


@pytest.fixture
def contexte(test_user):
    agent, organisme, recrutement, candidature = _grant(
        test_user, AgentOrganismeRole.SUPERVISEUR, None
    )
    return agent, candidature, _url(organisme.id, recrutement.pk, candidature.pk)


class TestAccess:
    @BOTH_METHODS
    def test_anonymous_access_is_unauthorized(self, api_client, method):
        response = _call(api_client, method, _url(uuid4(), uuid4(), uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @BOTH_METHODS
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.AGENT, None], ids=["no_recrutement_role", "no_role"]
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, method, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        recrutement, candidature = create_recrutement_with_candidature(organisme)

        response = _call(
            authenticated_client,
            method,
            _url(organisme.id, recrutement.pk, candidature.pk),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @BOTH_METHODS
    @UNKNOWN_OR_FOREIGN_IDS
    def test_returns_404_for(self, authenticated_client, test_user, method, build_ids):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement, candidature = create_recrutement_with_candidature(organisme)

        response = _call(
            authenticated_client,
            method,
            _url(*build_ids(organisme, recrutement, candidature)),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestListConversations:
    @AUTHORIZED_ROLES
    def test_authorized_agent_lists_conversations(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        _, organisme, recrutement, candidature = _grant(
            test_user, organisme_role, recrutement_role
        )
        _conversation_with_messages(candidature, "Bonjour")
        _conversation_with_messages(candidature, "Merci", "x" * 1000)

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.pk)
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["count"] == NB_CONVERSATIONS
        results = body["results"]
        assert set(results[0].keys()) == {
            "uuid",
            "objet",
            "creator",
            "created_at",
            "last_message_content",
            "last_message_author",
            "last_message_created_at",
        }
        dates = [result["last_message_created_at"] for result in results]
        assert dates == sorted(dates, reverse=True)
        assert all(
            len(result["last_message_content"])
            <= settings.CONVERSATION_LAST_MESSAGE_CONTENT_MAX_LENGTH
            for result in results
        )

    def test_limit_param_caps_page_size(self, authenticated_client, contexte):
        _, candidature, url = contexte
        for _ in range(TAILLE_PAGE_LIMITEE + 1):
            _conversation_with_messages(candidature, "Bonjour")

        response = authenticated_client.get(url, {"limit": TAILLE_PAGE_LIMITEE})

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert len(body["results"]) == TAILLE_PAGE_LIMITEE
        assert body["next"] is not None

    def test_lists_only_the_conversations_of_the_candidature(
        self, authenticated_client, contexte
    ):
        _, candidature, url = contexte
        _, autre_candidature = create_recrutement_with_candidature(
            candidature.etape.recrutement.organisme
        )
        conversation = _conversation_with_messages(candidature, "Bonjour")
        _conversation_with_messages(autre_candidature, "Bonjour")

        response = authenticated_client.get(url)

        assert [r["uuid"] for r in response.json()["results"]] == [str(conversation.pk)]

    def test_exposes_first_and_last_message_authors(
        self, authenticated_client, contexte
    ):
        _, candidature, url = contexte
        conversation = ConversationDjangoFactory(candidature=candidature)
        premier = MessageDjangoFactory(conversation=conversation, contenu="Premier")
        dernier = MessageDjangoFactory(conversation=conversation, contenu="Dernier")

        response = authenticated_client.get(url)

        (result,) = response.json()["results"]
        assert result["creator"] == premier.auteur.get_full_name()
        assert result["last_message_author"] == dernier.auteur.get_full_name()
        assert result["last_message_content"] == "Dernier"

    def test_default_page_size_is_20(self):
        assert ConversationPagination.page_size == TAILLE_PAGE_PAR_DEFAUT


class TestCreateConversation:
    @AUTHORIZED_ROLES
    def test_authorized_agent_creates_a_conversation(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        agent, organisme, recrutement, candidature = _grant(
            test_user, organisme_role, recrutement_role
        )

        response = _call(
            authenticated_client,
            "post",
            _url(organisme.id, recrutement.pk, candidature.pk),
        )

        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()
        assert body["objet"] == "Convocation"
        assert body["last_message_content"] == "Bonjour"
        assert body["creator"] == body["last_message_author"]
        message = MessageModel.objects.get(conversation_id=body["uuid"])
        assert message.auteur_id == agent.utilisateur_id

    def test_created_conversation_is_persisted_audited_and_listed(
        self, authenticated_client, contexte
    ):
        agent, candidature, url = contexte

        created = _call(authenticated_client, "post", url).json()

        conversation = ConversationModel.objects.get(pk=created["uuid"])
        assert conversation.candidature_id == candidature.pk
        assert conversation.objet == "Convocation"
        audit = AuditLogModel.objects.get(ressource_id=conversation.pk)
        assert audit.ressource_kind == "Conversation"
        assert audit.event_name == "ConversationCreee"
        assert audit.utilisateur_id == agent.utilisateur_id
        listed = authenticated_client.get(url).json()["results"]
        assert [c["uuid"] for c in listed] == [created["uuid"]]

    def test_attaches_max_documents_of_each_allowed_type_to_the_message(
        self, authenticated_client, contexte
    ):
        agent, candidature, url = contexte

        response = _call(authenticated_client, "post", url, documents=valid_documents())

        assert response.status_code == status.HTTP_201_CREATED
        pieces_jointes = MessageDocumentModel.objects.select_related("document").filter(
            message__conversation_id=response.json()["uuid"]
        )
        documents = [piece.document for piece in pieces_jointes]
        assert sorted(d.nom_original for d in documents) == [
            "cv.pdf",
            "diplome.pdf",
            "lettre.pdf",
            "photo.png",
            "scan.jpg",
        ]
        assert all(d.candidature_id == candidature.pk for d in documents)
        assert all(d.type_document == TypeDocument.AUTRE for d in documents)
        assert all(d.depose_par_id == agent.utilisateur_id for d in documents)

    def test_content_whitespace_is_preserved(self, authenticated_client, contexte):
        *_, url = contexte

        response = _call(authenticated_client, "post", url, content="    code\n")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["last_message_content"] == "    code\n"

    @pytest.mark.parametrize(
        "payload,champ",
        [
            ({"content": "Bonjour"}, "objet"),
            ({"objet": "Convocation"}, "content"),
            (_payload(objet=""), "objet"),
            (_payload(objet="a" * 256), "objet"),
            (_payload(content=""), "content"),
            (_payload(content=" \n\t"), "content"),
        ],
        ids=[
            "missing_objet",
            "missing_content",
            "blank_objet",
            "objet_too_long",
            "blank_content",
            "whitespace_only_content",
        ],
    )
    def test_invalid_payload_is_rejected(
        self, authenticated_client, contexte, payload, champ
    ):
        *_, url = contexte

        response = authenticated_client.post(url, payload, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert champ in response.json()
        assert not ConversationModel.objects.exists()

    @pytest.mark.parametrize("build_documents", INVALID_DOCUMENTS)
    def test_invalid_documents_are_rejected(
        self, authenticated_client, contexte, build_documents
    ):
        *_, url = contexte

        response = _call(authenticated_client, "post", url, documents=build_documents())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "documents" in response.json()

    def test_incomplete_uploaded_file_is_a_bad_request(
        self, authenticated_client, contexte
    ):
        *_, url = contexte

        with patch(
            "presentation.recruteur.views.candidature_conversations.create_conversation",
            side_effect=FichierDeposeIncomplet(),
        ):
            response = _call(authenticated_client, "post", url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": str(FichierDeposeIncomplet())}
