from typing import List

from django.db import DatabaseError, transaction
from django.db.models import F, Q
from django.utils import timezone

from domain.entities.concours import Concours
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.services.logger_interface import ILogger
from infrastructure.django_apps.shared.models.concours import ConcoursModel


class PostgresConcoursRepository(IConcoursRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for entity in concours_list:
            try:
                _, created_flag = ConcoursModel.objects.update_or_create(
                    id=entity.id,  # Use ID as the lookup key
                    defaults={
                        "nor_original": entity.nor_original.value,
                        "corps": entity.corps,
                        "grade": entity.grade,
                        "nor_list": [nor.value for nor in entity.nor_list],
                        "category": entity.category.value,
                        "ministry": entity.ministry.value,
                        "access_modality": [
                            modality.value for modality in entity.access_modality
                        ],
                        "written_exam_date": entity.written_exam_date,
                        "open_position_number": entity.open_position_number,
                    },
                )

                if created_flag:
                    created += 1
                else:
                    updated += 1

            except Exception as e:
                self.logger.error(
                    f"Failed to save Concours entity {entity.id}: {str(e)}"
                )
                error_detail: IUpsertError = {
                    "entity_id": entity.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_id(self, concours_id) -> Concours:
        try:
            concours_model = ConcoursModel.objects.get(id=concours_id)
            return concours_model.to_entity()
        except ConcoursModel.DoesNotExist as e:
            raise ConcoursDoesNotExist(str(concours_id)) from e

    def find_by_nor(self, nor) -> Concours:
        try:
            concours_model = ConcoursModel.objects.get(nor_original=nor.value)
            return concours_model.to_entity()
        except ConcoursModel.DoesNotExist as e:
            raise ConcoursDoesNotExist(str(nor)) from e

    def get_all(self) -> List[Concours]:
        concours_models = ConcoursModel.objects.all()
        return [model.to_entity() for model in concours_models]

    @transaction.atomic
    def get_pending_processing(self, limit: int = 1000) -> List[Concours]:
        qs = (
            ConcoursModel.objects.filter(archived_at__isnull=True, processing=False)
            .filter(Q(processed_at__isnull=True) | Q(updated_at__gt=F("processed_at")))
            .select_for_update(of=("self",), skip_locked=True)[:limit]
        )
        for obj in qs:
            obj.processing = True
        try:
            ConcoursModel.objects.bulk_update(qs, ["processing"])
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

        return [model.to_entity() for model in qs]

    def mark_as_processed(self, offers_list: List[Concours]) -> int:
        try:
            return ConcoursModel.objects.filter(
                id__in=[obj.id for obj in offers_list]
            ).update(processed_at=timezone.now(), processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e

    def mark_as_pending(self, offers_list: List[Concours]) -> int:
        try:
            return ConcoursModel.objects.filter(
                id__in=[obj.id for obj in offers_list]
            ).update(processing=False)
        except Exception as e:
            raise DatabaseError(f"Database error during update: {str(e)}") from e
