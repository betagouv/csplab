from collections.abc import Sequence
from datetime import datetime, timezone
from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.permission_service import (
    PermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import (
    CandidatureInexistante,
    MotifRefusRequis,
    RecrutementCandidatureInexistante,
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
) -> tuple[list[UUID], list[tuple[UUID, RecrutementCandidatureInexistante]]]:
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

        candidatures = list(CandidatureModel.objects.for_etape_change(candidature_ids))
        trouvees = {candidature.id for candidature in candidatures}
        manquantes = [id_ for id_ in candidature_ids if id_ not in trouvees]
        if manquantes:
            raise CandidatureInexistante(manquantes[0])

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

        reussites = [
            candidature.id
            for candidature in candidatures
            if candidature.etape.recrutement_id == recrutement.pk
        ]
        echecs = [
            (candidature.id, RecrutementCandidatureInexistante(candidature.id))
            for candidature in candidatures
            if candidature.etape.recrutement_id != recrutement.pk
        ]
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
