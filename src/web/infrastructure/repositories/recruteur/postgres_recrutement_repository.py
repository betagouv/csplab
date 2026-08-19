from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
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
            model = RecrutementModel.objects.get(  # type: ignore[attr-defined]
                pk=aggregate_id
            )
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

            EtapeModel.objects.bulk_create(
                [
                    EtapeModel(
                        id=etape.entity_id,
                        recrutement_id=recrutement.entity_id,
                        categorie=etape.categorie.value,
                        nom=etape.nom,
                    )
                    for etape in recrutement.etapes
                ],
                update_conflicts=True,
                update_fields=["categorie", "nom"],
                unique_fields=["id"],
            )

            EtapeModel.objects.filter(recrutement_id=recrutement.entity_id).exclude(
                id__in=[etape.entity_id for etape in recrutement.etapes]
            ).delete()
