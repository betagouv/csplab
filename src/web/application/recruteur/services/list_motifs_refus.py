from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus


def list_motifs_refus(
    *, organisme_id: UUID, utilisateur: Utilisateur
) -> list[MotifRefus]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_MOTIFS_REFUS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    return list(MotifRefus)
