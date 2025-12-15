"""Django implementation of IConcoursRepository."""

from typing import List, Optional

from apps.shared.infrastructure.adapters.persistence.models.concours import (
    ConcoursModel,
)
from core.entities.concours import Concours
from core.repositories.concours_repository_interface import IConcoursRepository
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult


class DjangoConcoursRepository(IConcoursRepository):
    """Django ORM implementation of IConcoursRepository."""

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
        created = 0
        updated = 0
        errors = []

        for concours in concours_list:
            try:
                _, was_created = ConcoursModel.objects.update_or_create(
                    id=concours.id,
                    defaults=ConcoursModel.from_entity(concours).__dict__,
                )

                if was_created:
                    created += 1
                else:
                    updated += 1

            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": concours.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_corps_id(self, corps_id: int) -> Optional[Concours]:
        """Find a Concours by its Corps ID."""
        try:
            concours_model = ConcoursModel.objects.get(corps_id=corps_id)
            return concours_model.to_entity()
        except ConcoursModel.DoesNotExist:
            return None

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        concours_models = ConcoursModel.objects.all()
        return [model.to_entity() for model in concours_models]

    def find_by_id(self, concours_id: int) -> Optional[Concours]:
        """Find a Concours by its ID."""
        try:
            concours_model = ConcoursModel.objects.get(id=concours_id)
            return concours_model.to_entity()
        except ConcoursModel.DoesNotExist:
            return None
