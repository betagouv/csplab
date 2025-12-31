"""Django implementation of IConcoursRepository."""

from typing import List, Optional

from apps.shared.infrastructure.adapters.persistence.models.concours import (
    ConcoursModel,
)
from core.repositories.concours_repository_interface import IConcoursRepository
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult
from domain.entities.concours import Concours


class DjangoConcoursRepository(IConcoursRepository):
    """Django ORM implementation of IConcoursRepository."""

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
                error_detail: IUpsertError = {
                    "entity_id": entity.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_id(self, concours_id: int) -> Optional[Concours]:
        """Find a Concours by its ID."""
        try:
            concours_model = ConcoursModel.objects.get(id=concours_id)
            return concours_model.to_entity()
        except ConcoursModel.DoesNotExist:
            return None

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        concours_models = ConcoursModel.objects.all()
        return [model.to_entity() for model in concours_models]
