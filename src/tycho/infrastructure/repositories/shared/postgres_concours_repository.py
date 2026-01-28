"""Django implementation of IConcoursRepository."""

from typing import List

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
    """Django ORM implementation of IConcoursRepository."""

    def __init__(self, logger: ILogger):
        """Initialize with logger."""
        self.logger = logger.get_logger(
            "INGESTION::REPOSITORY::PostgresConcoursRepository"
        )

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
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

    def find_by_id(self, concours_id: int) -> Concours:
        """Find a Concours by its ID."""
        try:
            concours_model = ConcoursModel.objects.get(id=concours_id)
            return concours_model.to_entity()
        except ConcoursModel.DoesNotExist as e:
            raise ConcoursDoesNotExist(concours_id) from e

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        concours_models = ConcoursModel.objects.all()
        return [model.to_entity() for model in concours_models]
