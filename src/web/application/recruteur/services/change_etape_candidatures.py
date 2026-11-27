from collections.abc import Sequence
from datetime import datetime, timezone
from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import (
    MotifRefusRequis,
    RecrutementEtapeInexistante,
    RecrutementInexistant,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import etapes_ordonnees
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def change_etape_candidatures(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
    etape_cible_id: UUID,
    candidature_ids: Sequence[UUID],
    motif_refus: str | None = None,
) -> tuple[list[UUID], list[tuple[UUID, CandidatureInaccessible]]]:
    PermissionService().authorize(
        action=PermissionAction.CHANGE_ETAPE_CANDIDATURES,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    with transaction.atomic():
        try:
            recrutement = (
                RecrutementModel.objects.active_by_id(recrutement_id)
                .filter(organisme_id=organisme_id)
                .select_for_update(of=("self",), no_key=True)
                .get()
            )
        except RecrutementModel.DoesNotExist as error:
            raise RecrutementInexistant(recrutement_id) from error

        reussites = list(
            CandidatureModel.objects.for_etape_change(
                recrutement.pk, candidature_ids
            ).values_list("id", flat=True)
        )
        trouvees = set(reussites)
        echecs = [
            (candidature_id, CandidatureInaccessible())
            for candidature_id in dict.fromkeys(candidature_ids)
            if candidature_id not in trouvees
        ]

        etape_cible = next(
            (
                etape
                for etape in etapes_ordonnees(recrutement)
                if etape.id == etape_cible_id
            ),
            None,
        )
        if etape_cible is None:
            raise RecrutementEtapeInexistante(
                etape_id=etape_cible_id, recrutement_id=recrutement_id
            )
        if etape_cible.motif_refus_required and not motif_refus:
            raise MotifRefusRequis(etape_id=etape_cible_id)

        CandidatureModel.objects.filter(pk__in=reussites).update(
            etape_id=etape_cible_id,
            motif_refus=motif_refus,
            updated_by_recruteur=datetime.now(tz=timezone.utc),
        )

        audit_log_writer = AuditLogWriter(repository=PostgresAuditLogRepository())
        for candidature_id in reussites:
            audit_log_writer.log_action(
                utilisateur_id=utilisateur.username,
                entity=Entity(entity_id=candidature_id),
                ressource_kind="CandidatureRecruteur",
                event_name="CandidatureEtapeModifiee",
            )
        audit_log_writer.log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=recrutement.pk),
            ressource_kind="Recrutement",
            event_name="EtapeCandidaturesChangees",
        )
    return reussites, echecs
