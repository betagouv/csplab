from unittest.mock import patch
from uuid import uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from domain.candidate.exceptions.document_errors import FichierDeposeIncomplet
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.document import DocumentQuerySet
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import (
    ConversationLectureModel,
    MessageModel,
    MessageQuerySet,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
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
    RecrutementDjangoFactory,
)
from presentation.recruteur.serializers import ConversationMessageSerializer
from tests.utils.conversation_views import AUTHORIZED_ROLES, HTTP_METHODS, grant
from tests.utils.message_documents import (
    INVALID_DOCUMENTS,
    PDF_BYTES,
    valid_documents,
)

TAILLE_PAGE_LIMITEE = 1
TAILLE_PAGE_PAR_DEFAUT = 25
MAX_PAGE_SIZE = 100
NB_MESSAGES = 3
NB_MESSAGES_AU_DELA_D_UNE_PAGE = TAILLE_PAGE_PAR_DEFAUT + 2


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
    _, autre_candidature = create_recrutement_with_candidature(organisme)
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


def _call(client, method, url):
    if method == "post":
        return client.post(url, {"content": "Bonjour"}, format="multipart")
    return client.get(url)


def _authorized_url(test_user, organisme_role, recrutement_role):
    _, organisme, recrutement, candidature = grant(
        test_user, organisme_role, recrutement_role
    )
    MessageDjangoFactory(conversation__candidature=candidature)  # other conversation
    return _url(
        organisme.id, recrutement.pk, candidature.pk, _conversation_of(candidature)
    )


def _superviseur_url(test_user):
    return _authorized_url(test_user, AgentOrganismeRole.SUPERVISEUR, None)


def _conversation_over_one_page(test_user):
    _, organisme, recrutement, candidature = grant(
        test_user, AgentOrganismeRole.SUPERVISEUR, None
    )
    conversation = ConversationDjangoFactory(candidature=candidature)
    messages = [
        MessageDjangoFactory(conversation=conversation, contenu=f"m{index}")
        for index in range(NB_MESSAGES_AU_DELA_D_UNE_PAGE)
    ]
    url = _url(organisme.id, recrutement.pk, candidature.pk, conversation.pk)
    return url, conversation, messages


def _contents(response):
    return [message["content"] for message in response.json()["results"]]


def _read_receipts(test_user):
    return ConversationLectureModel.objects.filter(utilisateur_id=test_user.username)


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
        recrutement, candidature = create_recrutement_with_candidature(organisme)

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
        assert not ConversationLectureModel.objects.exists()

    @HTTP_METHODS
    @pytest.mark.parametrize("build_ids", NOT_FOUND_CASES)
    def test_returns_404_for(self, authenticated_client, test_user, build_ids, method):
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
        assert not ConversationLectureModel.objects.exists()

    @pytest.mark.parametrize(
        "method,queryset_method", [("get", "by_conversation"), ("post", "create")]
    )
    def test_unexpected_error_is_a_server_error(
        self, authenticated_client, test_user, method, queryset_method
    ):
        url = _superviseur_url(test_user)

        with patch.object(
            MessageQuerySet, queryset_method, side_effect=RuntimeError("boom")
        ):
            response = _call(authenticated_client, method, url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    @AUTHORIZED_ROLES
    def test_authorized_agent_reads_conversation(
        self, authenticated_client, test_user, organisme_role, recrutement_role
    ):
        response = authenticated_client.get(
            _authorized_url(test_user, organisme_role, recrutement_role)
        )

        assert response.status_code == status.HTTP_200_OK
        results = response.json()["results"]
        assert len(results) == NB_MESSAGES
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

    def test_serves_the_latest_messages_oldest_first(
        self, authenticated_client, test_user
    ):
        url, _, messages = _conversation_over_one_page(test_user)

        response = authenticated_client.get(url)

        assert _contents(response) == [m.contenu for m in messages[2:]]
        assert len(_contents(response)) == TAILLE_PAGE_PAR_DEFAUT
        assert response.json()["previous"] is None
        older = authenticated_client.get(response.json()["next"])
        assert _contents(older) == ["m0", "m1"]
        assert older.json()["next"] is None

    def test_limit_cannot_exceed_the_max_page_size(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = grant(
            test_user, AgentOrganismeRole.SUPERVISEUR, None
        )
        conversation = ConversationDjangoFactory(candidature=candidature)
        MessageDjangoFactory.create_batch(MAX_PAGE_SIZE + 1, conversation=conversation)
        url = _url(organisme.id, recrutement.pk, candidature.pk, conversation.pk)

        response = authenticated_client.get(url, {"limit": MAX_PAGE_SIZE + 1})

        assert len(_contents(response)) == MAX_PAGE_SIZE
        assert response.json()["next"] is not None

    def test_reading_the_latest_messages_marks_the_conversation_as_read(
        self, authenticated_client, test_user
    ):
        url, conversation, messages = _conversation_over_one_page(test_user)

        authenticated_client.get(url)

        receipt = _read_receipts(test_user).get()
        assert receipt.conversation_id == conversation.pk
        assert receipt.read_at == messages[-1].created_at

    def test_reading_again_moves_the_receipt_forward(
        self, authenticated_client, test_user
    ):
        url, conversation, _ = _conversation_over_one_page(test_user)
        authenticated_client.get(url)
        new_message = MessageDjangoFactory(conversation=conversation)

        authenticated_client.get(url)

        receipt = _read_receipts(test_user).get()
        assert receipt.read_at == new_message.created_at

    def test_loading_older_messages_leaves_the_receipt_untouched(
        self, authenticated_client, test_user
    ):
        url, _, _ = _conversation_over_one_page(test_user)
        next_url = authenticated_client.get(url).json()["next"]
        _read_receipts(test_user).delete()

        response = authenticated_client.get(next_url)

        assert response.status_code == status.HTTP_200_OK
        assert not _read_receipts(test_user).exists()

    def test_head_request_does_not_mark_the_conversation_as_read(
        self, authenticated_client, test_user
    ):
        url, _, _ = _conversation_over_one_page(test_user)

        response = authenticated_client.head(url)

        assert response.status_code == status.HTTP_200_OK
        assert not _read_receipts(test_user).exists()

    def test_conversation_without_message_leaves_no_receipt(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = grant(
            test_user, AgentOrganismeRole.SUPERVISEUR, None
        )
        conversation = ConversationDjangoFactory(candidature=candidature)

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.pk, conversation.pk)
        )

        assert response.json()["results"] == []
        assert not _read_receipts(test_user).exists()

    def test_invalid_cursor_returns_404_without_marking_as_read(
        self, authenticated_client, test_user
    ):
        response = authenticated_client.get(
            _superviseur_url(test_user), {"cursor": "garbage"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not _read_receipts(test_user).exists()

    def test_serialization_error_does_not_mark_as_read(
        self, authenticated_client, test_user
    ):
        with patch.object(
            ConversationMessageSerializer,
            "to_representation",
            side_effect=RuntimeError("boom"),
        ):
            response = authenticated_client.get(_superviseur_url(test_user))

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert not _read_receipts(test_user).exists()

    def test_conversation_becomes_read_in_the_conversation_list(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = grant(
            test_user, AgentOrganismeRole.SUPERVISEUR, None
        )
        conversation = ConversationDjangoFactory(candidature=candidature)
        for index in range(NB_MESSAGES_AU_DELA_D_UNE_PAGE):
            MessageDjangoFactory(conversation=conversation, contenu=f"m{index}")
        list_url = reverse(
            "recruteur:organisme_recrutement_candidature_conversations",
            kwargs={
                "organisme_uuid": organisme.id,
                "recrutement_uuid": recrutement.pk,
                "candidature_uuid": candidature.pk,
            },
        )
        detail_url = _url(organisme.id, recrutement.pk, candidature.pk, conversation.pk)
        assert authenticated_client.get(list_url).json()["results"][0]["is_unread"]

        authenticated_client.get(detail_url)

        assert not authenticated_client.get(list_url).json()["results"][0]["is_unread"]

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
        pieces_jointes = message.pieces_jointes.select_related("document")

        documents = [piece.document for piece in pieces_jointes]
        assert len(documents) == len(created["documents"])

        cv = next(d for d in documents if d.nom_original == "cv.pdf")
        assert cv.type_document == TypeDocument.AUTRE
        assert cv.content_type == "application/pdf"
        assert cv.taille == len(PDF_BYTES)

        candidature_id = message.conversation.candidature_id
        assert all(d.candidature_id == candidature_id for d in documents)
        assert all(d.depose_par_id == test_user.username for d in documents)

        audit = AuditLogModel.objects.get(ressource_id=message.pk)
        assert audit.ressource_kind == "Message"
        assert audit.event_name == "MessageCree"
        assert audit.utilisateur_id == test_user.username

        listed = authenticated_client.get(url).json()["results"]
        assert listed[-1]["content"] == "Merci"
        assert listed[-1]["created_at"] == created["created_at"]
        assert len(listed) == NB_MESSAGES + 1  # the other conversation is excluded

    def test_incomplete_uploaded_file_is_a_bad_request(
        self, authenticated_client, test_user
    ):
        with patch.object(
            DocumentQuerySet, "build_from_upload", side_effect=FichierDeposeIncomplet()
        ):
            response = authenticated_client.post(
                _superviseur_url(test_user),
                {"content": "Bonjour", "documents": valid_documents()},
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
