from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.users.models import UserModel


def list_motifs_refus(
    *, organisme_id: UUID, utilisateur: UserModel
) -> list[MotifRefus]:
    OrganismePermissionService().can_execute(
        action=PermissionAction.GET_MOTIFS_REFUS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    return list(MotifRefus)
