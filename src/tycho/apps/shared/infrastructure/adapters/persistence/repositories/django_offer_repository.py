"""Django Offer repository implementation."""

from typing import List, Optional

from apps.shared.infrastructure.adapters.persistence.models.offer import OfferModel
from core.entities.offer import Offer
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult
from core.repositories.offer_repository_interface import IOfferRepository


class DjangoOfferRepository(IOfferRepository):
    """Django ORM implementation of Offer repository."""

    def upsert_batch(self, offers: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offer entities and return operation results."""
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for entity in offers:
            try:
                # Extract localisation fields
                region = (
                    entity.localisation.region.value
                    if entity.localisation and entity.localisation.region
                    else None
                )
                department = (
                    entity.localisation.department.value
                    if entity.localisation and entity.localisation.department
                    else None
                )

                # Extract limit_date value
                limit_date_value = (
                    entity.limit_date.value if entity.limit_date else None
                )

                _, created_flag = OfferModel.objects.update_or_create(
                    id=entity.id,
                    defaults={
                        "external_id": entity.external_id,
                        "titre": entity.titre,
                        "profile": entity.profile,
                        "category": entity.category.value if entity.category else None,
                        "verse": entity.verse.value if entity.verse else None,
                        "region": region,
                        "department": department,
                        "limit_date": limit_date_value,
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

    def find_by_id(self, offer_id: int) -> Optional[Offer]:
        """Find an Offer by its ID."""
        try:
            offer_model = OfferModel.objects.get(id=offer_id)
            return offer_model.to_entity()
        except OfferModel.DoesNotExist:
            return None
