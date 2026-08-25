from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.events.etapes_events import EtapeAjoutee, EtapeSupprimee
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.mappers.recrutement_mapper import RecrutementMapper


class PostgresRecrutementRepository(IRecrutementRepository):
    def __init__(self, mapper: RecrutementMapper) -> None:
        self.mapper = mapper

    def get_by_id(self, aggregate_id: UUID) -> Recrutement:
        try:
            model = RecrutementModel.objects.prefetch_related(  # type: ignore[attr-defined]
                "etapes__candidatures", "agents_liaisons"
            ).get(pk=aggregate_id)
            return self.mapper.to_domain(model)
        except ObjectDoesNotExist as e:
            raise RecrutementInexistant(aggregate_id) from e

    def save(self, recrutement: Recrutement) -> None:
        with transaction.atomic():
            recrutement_model = RecrutementModel.objects.select_for_update().get(
                offre_id=recrutement.entity_id
            )
            recrutement_model.ordre_etapes = self.mapper.from_domain(recrutement.etapes)
            recrutement_model.save()

            events = recrutement.read_events()

            # batch delete
            ids_to_delete = [
                e.aggregate_id for e in events if isinstance(e, EtapeSupprimee)
            ]
            if ids_to_delete:
                EtapeModel.objects.filter(id__in=ids_to_delete).delete()

            # batch create
            new_etapes = [
                e
                for e in recrutement.etapes
                if e.entity_id
                in {ev.aggregate_id for ev in events if isinstance(ev, EtapeAjoutee)}
            ]
            if new_etapes:
                EtapeModel.objects.bulk_create(
                    [
                        EtapeModel(
                            id=etape.entity_id,
                            recrutement_id=recrutement.entity_id,
                            categorie=etape.categorie.value,
                            nom=etape.nom,
                        )
                        for etape in new_etapes
                    ]
                )

            # todo batch_update will be done in update etapes usecase, nextPR
