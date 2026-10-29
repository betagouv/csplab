import logging
from datetime import datetime
from typing import List
from uuid import UUID

from django.db import DatabaseError, transaction
from django.utils import timezone
from referentiel.entities.organisme import Organisme
from referentiel.types import IUpsertError, IUpsertResult

from domain.commons.errors.organisme_errors import (
    OrganismeNexistePas,
    OrganismeSiretConflict,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository as IOrganismeIdentiteRepository,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper

logger = logging.getLogger(__name__)

# Each referentiel is the reference for its versant: DILA for FPE, FINESS for
# FPH, GIPCDG for FPT. When two referentiels claim the same SIRET, the first
# one in this list wins. An organisme outside these referentiels (created
# manually) is never overridden.
REFERENTIEL_PRIORITY = ("DILA", "FINESS", "GIPCDG")


def takes_precedence_over(referentiel: str | None, other: str | None) -> bool:
    if referentiel not in REFERENTIEL_PRIORITY or other not in REFERENTIEL_PRIORITY:
        return False
    return REFERENTIEL_PRIORITY.index(referentiel) < REFERENTIEL_PRIORITY.index(other)


class PostgresOrganismeRepository(IOrganismeIdentiteRepository):
    def __init__(self) -> None:
        self._mapper_identite = OrganismeIdentiteMapper()

    def create(self, organisme: Organisme) -> Organisme:
        model = self._mapper_identite.from_domain(organisme)
        model.save()
        if organisme.date_creation:
            OrganismeModel.objects.filter(pk=model.pk).update(
                created_at=organisme.date_creation
            )
        return organisme

    def get_by_id(self, organisme_id: UUID) -> Organisme:  # type: ignore[override]
        try:
            model = OrganismeModel.objects.get(id=organisme_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme_id)) from e
        return self._mapper_identite.to_domain(model)

    def save(self, organisme: Organisme) -> None:
        try:
            model = OrganismeModel.objects.get(id=organisme.entity_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme.entity_id)) from e
        self._mapper_identite.apply_to_model(model, organisme)
        model.save()

    def get_all(self) -> List[Organisme]:
        return [
            self._mapper_identite.to_domain(model)
            for model in OrganismeModel.objects.all()
        ]

    def get_ids_by_referentiel_and_external_id(
        self, pairs: list[tuple[str, str]]
    ) -> dict[tuple[str, str], UUID]:
        models = OrganismeModel.objects.by_referentiel_and_external_id_pairs(
            pairs
        ).only("id", "referentiel", "external_id")
        return {
            (str(model.referentiel), str(model.external_id)): model.id
            for model in models
        }

    def upsert_batch(self, organismes: list[Organisme]) -> IUpsertResult:
        try:
            with transaction.atomic():
                existing_ids = set(
                    OrganismeModel.objects.filter(
                        id__in=[organisme.entity_id for organisme in organismes]
                    )
                    .select_for_update(of=("self",))
                    .values_list("id", flat=True)
                )

                organismes, replaced_by, errors = self._resolve_siret_conflicts(
                    organismes
                )
                self._replace(replaced_by)

                new_models = []
                models_to_update = []
                for organisme in organismes:
                    model = self._mapper_identite.from_domain(organisme)
                    if organisme.entity_id in existing_ids:
                        model.updated_at = timezone.make_aware(datetime.now())
                        models_to_update.append(model)
                    else:
                        new_models.append(model)

                created = 0
                if new_models:
                    created = len(OrganismeModel.objects.bulk_create(new_models))

                updated = 0
                if models_to_update:
                    updated = OrganismeModel.objects.bulk_update(
                        models_to_update,
                        fields=[
                            "nom",
                            "versant",
                            "siret",
                            "parent_id",
                            "localisation",
                            "external_id",
                            "referentiel",
                            "millesime",
                            "gestion_ats",
                            "date_creation",
                            "date_derniere_activite",
                            "updated_at",
                        ],
                    )

            return {"created": created, "updated": updated, "errors": errors}
        except Exception as e:
            raise DatabaseError(f"Database error during bulk upsert: {e}") from e

    def _resolve_siret_conflicts(
        self, organismes: list[Organisme]
    ) -> tuple[list[Organisme], dict[UUID, UUID], list[IUpsertError]]:
        holders = {
            model.siret: model
            for model in OrganismeModel.objects.holding_sirets(
                sirets=[str(organisme.siret) for organisme in organismes],
                excluding_ids=[organisme.entity_id for organisme in organismes],
            ).select_for_update(of=("self",))
        }

        kept = []
        replaced_by: dict[UUID, UUID] = {}
        errors: list[IUpsertError] = []
        for organisme in organismes:
            holder = holders.get(str(organisme.siret))
            if holder is None:
                kept.append(organisme)
            elif takes_precedence_over(organisme.referentiel, holder.referentiel):
                replaced_by[holder.id] = organisme.entity_id
                kept.append(organisme)
            else:
                conflict = OrganismeSiretConflict(organisme, holder)
                logger.warning(str(conflict))
                errors.append(
                    {
                        "entity_id": organisme.entity_id,
                        "error": str(conflict),
                        "exception": conflict,
                    }
                )

        return kept, replaced_by, errors

    def _replace(self, replaced_by: dict[UUID, UUID]) -> None:
        for holder in OrganismeModel.objects.filter(id__in=replaced_by):
            target_id = replaced_by[holder.id]
            holder.move_dependents_to(target_id)
            logger.info(
                "Organisme %s (%s %s) merged into %s, which takes SIRET %s",
                holder.id,
                holder.referentiel,
                holder.external_id,
                target_id,
                holder.siret,
            )
        OrganismeModel.objects.filter(id__in=replaced_by).delete()

    def get_by_referentiel_and_external_id_batch(
        self, pairs: list[tuple[str, str]]
    ) -> dict[tuple[str, str], Organisme]:
        models = OrganismeModel.objects.by_referentiel_and_external_id_pairs(
            pairs
        ).not_supprimes()
        return {
            (
                str(model.referentiel),
                str(model.external_id),
            ): self._mapper_identite.to_domain(model)
            for model in models
        }

    def supprimer_batch(self, organismes: list[Organisme]) -> int:
        if not organismes:
            return 0

        ids = [organisme.entity_id for organisme in organismes]
        return (
            OrganismeModel.objects.filter(id__in=ids)
            .not_supprimes()
            .update(supprime_le=timezone.now())
        )
