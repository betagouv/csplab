from uuid import UUID, uuid4

from django.db import IntegrityError, transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.tag_errors import (
    TagAlreadyOnNote,
    TagCategoryMismatch,
    TagNotFound,
)
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.tag.models import NoteTagModel, TagCategory, TagModel
from infrastructure.django_apps.users.models import UserModel


def add_note_tag(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    note_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
) -> None:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_NOTE,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    candidature_service = CandidatureAgentService(
        recrutement_id=recrutement_id, candidature_id=candidature_id
    )
    candidature_service.check_candidature_belongs_to_recrutement()

    with transaction.atomic():
        try:
            note = (
                NoteModel.objects.by_candidature_author_and_id(
                    candidature_id, utilisateur.username, note_id
                )
                .select_for_update(of=("self",))
                .get()
            )
        except NoteModel.DoesNotExist as error:
            raise NoteIntrouvable(note_id) from error

        try:
            tag = TagModel.objects.by_id(organisme_id, tag_id).select_for_update().get()
        except TagModel.DoesNotExist as error:
            raise TagNotFound(tag_id) from error

        if tag.category != TagCategory.NOTE:
            raise TagCategoryMismatch(tag_id)

        try:
            NoteTagModel.objects.create(id=uuid4(), note=note, tag=tag)
        except IntegrityError as error:
            raise TagAlreadyOnNote(tag_id) from error
