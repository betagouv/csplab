from datetime import datetime
from typing import Dict, List

from django.db import DatabaseError, transaction
from django.utils import timezone

from domain.entities.metier import Metier
from domain.exceptions.domain_errors import MetierDoesNotExist
from domain.repositories.document_repository_interface import IUpsertResult
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.services.logger_interface import ILogger
from infrastructure.django_apps.shared.models.metier import MetierModel


class PostgresMetierRepository(IMetierRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult:
        try:
            with transaction.atomic():
                # Utiliser str(metier.id) comme external_id pour les entités du domaine
                existing_models = list(
                    MetierModel.objects.filter(
                        external_id__in=[str(metier.id) for metier in metiers]
                    ).select_for_update(of=("self",))
                )

                existing_models_map = {
                    model.external_id: model for model in existing_models
                }
                existing_external_ids = set(existing_models_map.keys())

                partitioned: Dict[str, List[Metier]] = {"new": [], "existing": []}
                for metier in metiers:
                    metier_external_id = str(metier.id)
                    if metier_external_id in existing_external_ids:
                        partitioned["existing"].append(metier)
                    else:
                        partitioned["new"].append(metier)

                created = 0
                updated = 0

                if partitioned["new"]:
                    new_models = []
                    for metier in partitioned["new"]:
                        model = MetierModel.from_entity(metier)
                        new_models.append(model)

                    created_models = MetierModel.objects.bulk_create(
                        new_models, ignore_conflicts=True
                    )
                    created = len(created_models)

                if partitioned["existing"]:
                    models_to_update = []
                    for metier in partitioned["existing"]:
                        metier_external_id = str(metier.id)
                        if metier_external_id in existing_models_map:
                            existing_model = existing_models_map[metier_external_id]
                            updated_model = MetierModel.from_entity(metier)
                            updated_model.id = existing_model.id
                            updated_model.updated_at = timezone.make_aware(
                                datetime.now()
                            )
                            models_to_update.append(updated_model)

                    if models_to_update:
                        updated = MetierModel.objects.bulk_update(
                            models_to_update,
                            fields=[
                                "libelle_court",
                                "libelle_long",
                                "definition_synthetique",
                                "code_domaine_fonctionnel",
                                "versants",
                                "activites",
                                "competences",
                                "conditions_particulieres",
                                "updated_at",
                            ],
                        )

            return {"created": created, "updated": updated, "errors": []}

        except Exception as e:
            self.logger.error("Database error during bulk upsert: %s", str(e))
            raise DatabaseError("Database error during bulk upsert: %s", str(e)) from e

    def find_by_external_id(self, external_id: str) -> Metier:
        try:
            metier_model = MetierModel.objects.get(external_id=external_id)
            return metier_model.to_entity()
        except MetierModel.DoesNotExist as e:
            raise MetierDoesNotExist(
                f"Metier with external_id {external_id} not found"
            ) from e
