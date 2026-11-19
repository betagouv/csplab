from collections.abc import Sequence
from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.errors.application_errors_recruteur import (
    RecrutementEtapeIncoherents,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementInexistant,
    SupressionEtapeImpossible,
)
from domain.recruteur.etapes_rules import valider_sequence_etapes
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_recrutement_etapes(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
    etapes: Sequence[EtapeData],
) -> list[EtapeModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    valider_sequence_etapes(etapes)
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

        anciennes = etapes_ordonnees(
            recrutement, recrutement.etapes.with_nb_candidatures()
        )
        anciennes_par_id = {etape.id: etape for etape in anciennes}
        rang_ancien = {etape.id: rang for rang, etape in enumerate(anciennes)}

        finales: list[EtapeModel] = []
        ajoutees: list[EtapeModel] = []
        renommees: list[EtapeModel] = []
        journal: list[tuple[UUID, str]] = []
        for rang, etape_data in enumerate(etapes):
            if etape_data.etape_uuid is None:
                etape = EtapeModel(
                    id=uuid4(),
                    recrutement=recrutement,
                    categorie=etape_data.categorie.value,
                    nom=etape_data.nom,
                )
                ajoutees.append(etape)
                journal.append((etape.id, "EtapeAjoutee"))
            else:
                etape = _etape_existante(
                    anciennes_par_id,
                    etape_uuid=etape_data.etape_uuid,
                    categorie=etape_data.categorie,
                    recrutement_id=recrutement_id,
                )
                if etape.nom != etape_data.nom:
                    etape.nom = etape_data.nom
                    renommees.append(etape)
                    journal.append((etape.id, "EtapeRenommee"))
                if rang_ancien[etape.id] != rang:
                    journal.append((etape.id, "EtapeReordonnee"))
            finales.append(etape)

        conservees = {etape.id for etape in finales}
        supprimees = [etape for etape in anciennes if etape.id not in conservees]
        for etape in supprimees:
            nb_candidatures = etape.nb_candidatures  # type: ignore[attr-defined]
            if nb_candidatures:
                raise SupressionEtapeImpossible(
                    etape_id=etape.id, nombre_candidatures=nb_candidatures
                )
        journal += [(etape.id, "EtapeSupprimee") for etape in supprimees]

        EtapeModel.objects.filter(pk__in=[etape.pk for etape in supprimees]).delete()
        EtapeModel.objects.bulk_create(ajoutees)
        for etape in renommees:
            etape.save(update_fields=["nom", "updated_at"])
        recrutement.ordre_etapes = [str(etape.id) for etape in finales]
        recrutement.save(update_fields=["ordre_etapes", "updated_at"])

        audit_log_writer = AuditLogWriter(repository=PostgresAuditLogRepository())
        for etape_id, event_name in journal:
            audit_log_writer.log_action(
                utilisateur_id=utilisateur.username,
                entity=Entity(entity_id=etape_id),
                ressource_kind="EtapeRecrutement",
                event_name=event_name,
            )
        audit_log_writer.log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=recrutement.pk),
            ressource_kind="Recrutement",
            event_name="RecrutementEtapesMisesAJour",
        )
    return finales


def _etape_existante(
    anciennes_par_id: dict[UUID, EtapeModel],
    *,
    etape_uuid: UUID,
    categorie: CategorieEtapeRecrutement,
    recrutement_id: UUID,
) -> EtapeModel:
    etape = anciennes_par_id.get(etape_uuid)
    if etape is None:
        raise RecrutementEtapeIncoherents(
            recrutement_id=recrutement_id, etape_id=etape_uuid
        )
    if etape.categorie != categorie.value:
        raise ConfigurationEtapesInvalide(
            "La catégorie d'une étape existante ne peut pas changer"
        )
    return etape
