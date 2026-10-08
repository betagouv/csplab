from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import (
    RecrutementInexistant,
    SupressionEtapeImpossible,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def initialize_recrutement_etapes(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> list[EtapeModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.INIT_RECRUTEMENT_ETAPES,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    with transaction.atomic():
        try:
            recrutement = (
                RecrutementModel.objects.active_by_id(recrutement_id)
                .with_organisme()
                .select_for_update(of=("self",), no_key=True)
                .get()
            )
        except RecrutementModel.DoesNotExist as error:
            raise RecrutementInexistant(recrutement_id) from error
        if recrutement.organisme_id != organisme_id:
            raise OrganismeRecrutementIncoherents(organisme_id, recrutement_id)

        anciennes = etapes_ordonnees(
            recrutement, recrutement.etapes.with_nb_candidatures()
        )
        for etape in anciennes:
            nb_candidatures = etape.nb_candidatures  # type: ignore[attr-defined]
            if nb_candidatures:
                raise SupressionEtapeImpossible(
                    etape_id=etape.id, nombre_candidatures=nb_candidatures
                )
        recrutement.etapes.filter(pk__in=[etape.pk for etape in anciennes]).delete()
        nouvelles = EtapeModel.objects.bulk_create(
            EtapeModel(
                id=uuid4(),
                recrutement=recrutement,
                categorie=CategorieEtapeRecrutement(etape["categorie"]).value,
                nom=etape["nom"],
            )
            for etape in recrutement.organisme.etapes or []
        )
        recrutement.ordre_etapes = [str(etape.id) for etape in nouvelles]
        recrutement.save(update_fields=["ordre_etapes", "updated_at"])

        audit_log_writer = AuditLogWriter(repository=PostgresAuditLogRepository())
        for etape, event_name in [
            *((etape, "EtapeSupprimee") for etape in anciennes),
            *((etape, "EtapeAjoutee") for etape in nouvelles),
        ]:
            audit_log_writer.log_action(
                utilisateur_id=utilisateur.username,
                entity=Entity(entity_id=etape.id),
                ressource_kind="EtapeRecrutement",
                event_name=event_name,
            )
        audit_log_writer.log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=recrutement.pk),
            ressource_kind="Recrutement",
            event_name="RecrutementEtapesReinitialisees",
        )
    return nouvelles
