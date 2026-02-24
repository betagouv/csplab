from typing import List
from uuid import UUID

from django.db import DatabaseError, transaction
from django.db.models import F, Q
from django.utils import timezone

from domain.entities.corps import Corps
from domain.exceptions.corps_errors import CorpsDoesNotExist
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.services.logger_interface import ILogger
from infrastructure.django_apps.shared.models.corps import CorpsModel


class PostgresCorpsRepository(ICorpsRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def upsert_batch(self, corps: List[Corps]) -> IUpsertResult:
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for entity in corps:
            try:
                _, created_flag = CorpsModel.objects.update_or_create(
                    id=entity.id,  # Use ID as the lookup key
                    defaults={
                        "code": entity.code,
                        "category": entity.category.value if entity.category else None,
                        "ministry": entity.ministry.value,
                        "diploma_level": entity.diploma.value
                        if entity.diploma
                        else None,
                        "short_label": entity.label.short_value,
                        "long_label": entity.label.value,
                        "access_modalities": [
                            modality.value for modality in entity.access_modalities
                        ],
                    },
                )

                if created_flag:
                    created += 1
                else:
                    updated += 1

            except Exception as e:
                self.logger.error(f"Failed to save Corps entity {entity.id}: {str(e)}")
                error_detail: IUpsertError = {
                    "entity_id": entity.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_id(self, corps_id: UUID) -> Corps:
        try:
            corps_model = CorpsModel.objects.get(id=corps_id)
            return corps_model.to_entity()
        except CorpsModel.DoesNotExist as e:
            raise CorpsDoesNotExist(corps_id) from e

    def find_by_code(self, code: str) -> Corps:
        try:
            corps_model = CorpsModel.objects.get(code=code)
            return corps_model.to_entity()
        except CorpsModel.DoesNotExist as e:
            raise CorpsDoesNotExist(code) from e

    def get_all(self) -> List[Corps]:
        corps_models = CorpsModel.objects.all()
        return [corps_model.to_entity() for corps_model in corps_models]

    @transaction.atomic
    def get_pending_processing(self, limit: int = 1000) -> List[Corps]:
        qs = (
            CorpsModel.objects.filter(archived_at__isnull=True, processing=False)
            .filter(Q(processed_at__isnull=True) | Q(updated_at__gt=F("processed_at")))
            .select_for_update(of=("self",), skip_locked=True)[:limit]
        )

        for obj in qs:
            obj.processing = True
        try:
            CorpsModel.objects.bulk_update(qs, ["processing"])
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

        return [model.to_entity() for model in qs]

    def mark_as_processed(self, offers_list: List[Corps]) -> int:
        try:
            return CorpsModel.objects.filter(
                id__in=[obj.id for obj in offers_list]
            ).update(processed_at=timezone.now(), processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

    def mark_as_pending(self, offers_list: List[Corps]) -> int:
        try:
            return CorpsModel.objects.filter(
                id__in=[obj.id for obj in offers_list]
            ).update(processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e
