from uuid import UUID

from application.identite.context_services.permission_service import (
    PermissionService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.users.models import UserModel


def list_motifs_refus(
    *, organisme_id: UUID, utilisateur: UserModel
) -> list[MotifRefus]:
    PermissionService().authorize(
        action=PermissionAction.GET_MOTIFS_REFUS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    return list(MotifRefus)
