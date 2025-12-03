"""Django Corps repository implementation."""

from typing import List, Optional

from apps.ingestion.infrastructure.adapters.persistence.models.corps import CorpsModel
from core.entities.corps import Corps
from core.repositories.corps_repository_interface import ICorpsRepository
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult


class DjangoCorpsRepository(ICorpsRepository):
    """Django ORM implementation of Corps repository."""

    def upsert(self, corps: Corps) -> Corps:
        """Insert or update a single Corps entity."""
        corps_model, _ = CorpsModel.objects.update_or_create(
            id=corps.id,
            defaults={
                "code": corps.code,
                "category": corps.category.value,
                "ministry": corps.ministry.value,
                "diploma_level": corps.diploma.value if corps.diploma else None,
                "short_label": corps.label.short_value,
                "long_label": corps.label.value,
                "access_modalities": [
                    modality.value for modality in corps.access_modalities
                ],
            },
        )
        return corps_model.to_entity()

    def upsert_batch(self, corps: List[Corps]) -> IUpsertResult:
        """Insert or update multiple Corps entities and return operation results."""
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for entity in corps:
            try:
                corps_model, created_flag = CorpsModel.objects.update_or_create(
                    id=entity.id,
                    defaults={
                        "code": entity.code,
                        "category": entity.category.value,
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
                error_detail: IUpsertError = {
                    "entity_id": entity.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
        }

    def find_by_id(self, corps_id: int) -> Optional[Corps]:
        """Find a Corps by its ID."""
        try:
            corps_model = CorpsModel.objects.get(id=corps_id)
            return corps_model.to_entity()
        except CorpsModel.DoesNotExist:
            return None
