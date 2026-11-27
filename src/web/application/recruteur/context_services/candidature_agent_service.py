import logging
from uuid import UUID

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
    OrganismePermissionError,
)
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.messagerie.models import ConversationModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel

logger = logging.getLogger(__name__)

_CAUSES_CANDIDATURE_INACCESSIBLE = (
    OperationOrganismeRefusee,
    OrganismeNexistePas,
    OrganismePermissionError,
    RecrutementInexistant,
    RecrutementCandidatureInexistante,
)


class CandidatureAgentService:
    def __init__(
        self,
        *,
        organisme_id: UUID,
        recrutement_id: UUID,
        candidature_id: UUID,
        utilisateur: UserModel,
    ) -> None:
        self.organisme_id = organisme_id
        self.recrutement_id = recrutement_id
        self.candidature_id = candidature_id
        self.utilisateur = utilisateur

    def check_accessible(
        self, action: PermissionAction, *, check_candidature: bool = True
    ) -> AgentOrganismeRole:
        try:
            organisme_role = PermissionService().authorize(
                action=action,
                utilisateur=self.utilisateur,
                organisme_id=self.organisme_id,
                recrutement_id=self.recrutement_id,
            )
            if organisme_role is None:
                raise OperationOrganismeRefusee()
            self._check_recrutement()
            if check_candidature:
                self._check_candidature()
        except _CAUSES_CANDIDATURE_INACCESSIBLE as exc:
            raise self.inaccessible(exc) from exc
        return organisme_role

    def check_exists(self) -> None:
        try:
            if not OrganismeModel.objects.by_id(self.organisme_id).exists():
                raise OrganismeNexistePas(str(self.organisme_id))
            self._check_recrutement()
            self._check_candidature()
        except _CAUSES_CANDIDATURE_INACCESSIBLE as exc:
            raise self.inaccessible(exc) from exc

    def lock_candidature(self) -> None:
        if (
            CandidatureModel.objects.by_recrutement_and_candidature(
                self.recrutement_id, self.candidature_id
            )
            .select_for_update(of=("self",))
            .values_list("pk", flat=True)
            .first()
            is None
        ):
            cause = RecrutementCandidatureInexistante(self.candidature_id)
            raise self.inaccessible(cause) from cause

    def check_conversation_belongs_to_candidature(self, conversation_id: UUID) -> None:
        if not ConversationModel.objects.by_candidature_and_id(
            self.candidature_id, conversation_id
        ).exists():
            raise ConversationInexistante(conversation_id)

    def inaccessible(self, cause: Exception) -> CandidatureInaccessible:
        logger.info(
            "Candidature %s inaccessible : %s (%s)",
            self.candidature_id,
            type(cause).__name__,
            cause,
        )
        return CandidatureInaccessible()

    def _check_recrutement(self) -> None:
        RecrutementAgentService(
            organisme_id=self.organisme_id, recrutement_id=self.recrutement_id
        ).check_recrutement_belongs_to_organisme()

    def _check_candidature(self) -> None:
        if not CandidatureModel.objects.by_recrutement_and_candidature(
            self.recrutement_id, self.candidature_id
        ).exists():
            raise RecrutementCandidatureInexistante(self.candidature_id)
