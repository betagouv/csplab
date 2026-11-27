from uuid import uuid4

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageModel,
)
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.tag.models import CandidatureTagModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)

MESSAGE = "Cette candidature n'est pas accessible."

ENDPOINTS = [
    pytest.param(
        "organisme_recrutement_candidature_detail", "get", {}, None, id="detail"
    ),
    pytest.param("candidature_notes", "get", {}, None, id="notes-list"),
    pytest.param(
        "candidature_notes", "post", {}, {"message": "Note"}, id="notes-create"
    ),
    pytest.param(
        "candidature_note_detail",
        "patch",
        {"note_uuid": uuid4},
        {"message": "Note"},
        id="note-update",
    ),
    pytest.param(
        "candidature_note_detail",
        "delete",
        {"note_uuid": uuid4},
        None,
        id="note-delete",
    ),
    pytest.param(
        "candidature_note_visibilite",
        "put",
        {"note_uuid": uuid4},
        {"est_privee": True},
        id="note-visibilite",
    ),
    pytest.param(
        "candidature_note_tags",
        "post",
        {"note_uuid": uuid4},
        {"tag_uuid": str(uuid4())},
        id="note-tag-add",
    ),
    pytest.param(
        "candidature_note_tag",
        "delete",
        {"note_uuid": uuid4, "tag_uuid": uuid4},
        None,
        id="note-tag-remove",
    ),
    pytest.param(
        "candidature_tags",
        "post",
        {},
        {"tag_uuid": str(uuid4())},
        id="candidature-tag-add",
    ),
    pytest.param(
        "candidature_tag",
        "delete",
        {"tag_uuid": uuid4},
        None,
        id="candidature-tag-remove",
    ),
    pytest.param(
        "organisme_recrutement_candidature_documents", "get", {}, None, id="documents"
    ),
    pytest.param(
        "organisme_recrutement_candidature_document",
        "get",
        {"document_uuid": uuid4},
        None,
        id="document",
    ),
    pytest.param(
        "organisme_recrutement_candidature_conversations",
        "get",
        {},
        None,
        id="conversations-list",
    ),
    pytest.param(
        "organisme_recrutement_candidature_conversations",
        "post",
        {},
        {"objet": "Objet", "content": "Bonjour"},
        id="conversation-create",
    ),
    pytest.param(
        "organisme_recrutement_candidature_conversation_detail",
        "get",
        {"conversation_uuid": uuid4},
        None,
        id="conversation-read",
    ),
    pytest.param(
        "organisme_recrutement_candidature_conversation_detail",
        "post",
        {"conversation_uuid": uuid4},
        {"content": "Bonjour"},
        id="conversation-reply",
    ),
]


def _unknown_organisme(test_user):
    return uuid4(), uuid4(), uuid4()


def _caller_without_organisme_role(test_user):
    _, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=None)
    )
    return organisme.id, recrutement.pk, candidature.id


def _agent_not_member_of_recrutement(test_user):
    _, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.AGENT, utilisateur=test_user
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return organisme.id, recrutement.pk, candidature.id


def _recrutement_not_in_organisme(test_user):
    _, organisme, _recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=test_user)
    )
    return organisme.id, RecrutementDjangoFactory().pk, candidature.id


def _candidature_of_another_recrutement(test_user):
    _, organisme, recrutement, _candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=test_user)
    )
    return organisme.id, recrutement.pk, CandidatureDjangoFactory().id


def _deleted_organisme(test_user):
    _, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=test_user)
    )
    OrganismeModel.objects.filter(pk=organisme.pk).update(supprime_le=timezone.now())
    return organisme.id, recrutement.pk, candidature.id


def _absent_candidature(test_user):
    _, organisme, recrutement, _candidature = (
        create_recrutement_and_candidature_for_agent(utilisateur=test_user)
    )
    return organisme.id, recrutement.pk, uuid4()


CASES = [
    pytest.param(_unknown_organisme, id="unknown_organisme"),
    pytest.param(_caller_without_organisme_role, id="caller_without_organisme_role"),
    pytest.param(
        _agent_not_member_of_recrutement, id="agent_not_member_of_recrutement"
    ),
    pytest.param(_recrutement_not_in_organisme, id="recrutement_not_in_organisme"),
    pytest.param(
        _candidature_of_another_recrutement, id="candidature_of_another_recrutement"
    ),
    pytest.param(_deleted_organisme, id="deleted_organisme"),
    pytest.param(_absent_candidature, id="absent_candidature"),
]


@pytest.mark.parametrize(("name", "method", "extra", "data"), ENDPOINTS)
@pytest.mark.parametrize("build_ids", CASES)
def test_inaccessible_candidature_gets_the_same_not_found(
    authenticated_client, test_user, name, method, extra, data, build_ids
):
    organisme_id, recrutement_id, candidature_id = build_ids(test_user)
    url = reverse(
        f"recruteur:{name}",
        kwargs={
            "organisme_uuid": organisme_id,
            "recrutement_uuid": recrutement_id,
            "candidature_uuid": candidature_id,
            **{key: make() for key, make in extra.items()},
        },
    )

    response = getattr(authenticated_client, method)(
        url, data=data, format="multipart" if "conversation" in name else "json"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": MESSAGE}
    assert not AuditLogModel.objects.exists()
    assert not NoteModel.objects.exists()
    assert not CandidatureTagModel.objects.exists()
    assert not ConversationModel.objects.exists()
    assert not MessageModel.objects.exists()
