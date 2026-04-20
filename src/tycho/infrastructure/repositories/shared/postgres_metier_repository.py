from datetime import datetime
from typing import Dict, List

from django.db import DatabaseError, transaction
from django.utils import timezone

from domain.entities.document import Document
from domain.entities.metier import Metier
from domain.exceptions.domain_errors import MetierDoesNotExist
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.services.logger_interface import ILogger
from infrastructure.django_apps.shared.models.metier import MetierModel
from infrastructure.external_gateways.dtos.ingres_metiers_dtos import (
    IngresMetiersDocument,
)


class PostgresMetierRepository(IMetierRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult:
        try:
            with transaction.atomic():
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

    def get_all(self) -> List[Metier]:
        metier_models = MetierModel.objects.all()
        return [model.to_entity() for model in metier_models]

    def get_pending_processing(self, limit: int = 1000) -> List[Metier]:
        metier_models = MetierModel.objects.filter(
            processing=False, processed_at__isnull=True
        )[:limit]
        return [model.to_entity() for model in metier_models]

    def mark_as_processed(self, metiers_list: List[Metier]) -> int:
        metier_ids = [metier.id for metier in metiers_list]
        return MetierModel.objects.filter(id__in=metier_ids).update(
            processing=False, processed_at=timezone.now()
        )

    def mark_as_pending(self, metiers_list: List[Metier]) -> int:
        metier_ids = [metier.id for metier in metiers_list]
        return MetierModel.objects.filter(id__in=metier_ids).update(
            processing=True, processed_at=None
        )

    def upsert_batch_rich_data(self, raw_documents: List[Document]) -> IUpsertResult:
        if not raw_documents:
            return {"created": 0, "updated": 0, "errors": []}

        # Extract external_ids from raw documents
        external_ids = []
        valid_documents = []
        errors = []

        for document in raw_documents:
            try:
                dto = IngresMetiersDocument(**document.raw_data)
                external_ids.append(dto.identifiant)
                valid_documents.append((document, dto))
            except Exception as e:
                error_msg = f"Error processing document {document.id}: {str(e)}"
                self.logger.error(error_msg)
                error_detail: IUpsertError = {
                    "entity_id": document.id,
                    "error": error_msg,
                    "exception": e,
                }
                errors.append(error_detail)
                continue

        if not valid_documents:
            return {"created": 0, "updated": 0, "errors": errors}

        try:
            with transaction.atomic():
                # Check which external_ids already exist
                existing_external_ids = set(
                    MetierModel.objects.filter(
                        external_id__in=external_ids
                    ).values_list("external_id", flat=True)
                )

                # Prepare models for creation
                models_to_create = []
                models_to_update = []

                for document, dto in valid_documents:
                    try:
                        model_data = MetierModel._dto_to_model_data(dto)

                        if dto.identifiant in existing_external_ids:
                            models_to_update.append(model_data)
                        else:
                            model = MetierModel(**model_data)
                            models_to_create.append(model)
                    except Exception as e:
                        error_msg = (
                            f"Error creating model for document {document.id}: {str(e)}"
                        )
                        self.logger.error(error_msg)
                        model_error: IUpsertError = {
                            "entity_id": document.id,
                            "error": error_msg,
                            "exception": e,
                        }
                        errors.append(model_error)
                        continue

                created_count = 0
                if models_to_create:
                    created_models = MetierModel.objects.bulk_create(
                        models_to_create, ignore_conflicts=True
                    )
                    created_count = len(created_models)

                updated_count = len(models_to_update)

                return {
                    "created": created_count,
                    "updated": updated_count,
                    "errors": errors,
                }

        except Exception as e:
            error_msg = f"Database error during bulk upsert: {str(e)}"
            self.logger.error(error_msg)
            bulk_error: IUpsertError = {
                "entity_id": "bulk_operation",
                "error": error_msg,
                "exception": e,
            }
            errors.append(bulk_error)
            raise DatabaseError(error_msg) from e
