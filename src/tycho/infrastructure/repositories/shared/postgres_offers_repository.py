"""Django implementation of IOffersRepository."""

from typing import List, Optional

from domain.entities.offer import Offer
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.repositories.offers_repository_interface import IOffersRepository
from infrastructure.django_apps.shared.models.offer import OfferModel


class PostgresOffersRepository(IOffersRepository):
    """Django ORM implementation of IOffersRepository."""

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offer entities and return operation results."""
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for entity in offers_list:
            try:
                # Extract localisation fields
                region = None
                department = None
                if entity.localisation:
                    region = entity.localisation.region.value
                    department = entity.localisation.department.value

                # Extract limit_date
                limit_date = None
                if entity.limit_date:
                    limit_date = entity.limit_date.value

                _, created_flag = OfferModel.objects.update_or_create(
                    id=entity.id,  # Use ID as the lookup key
                    defaults={
                        "external_id": entity.external_id,
                        "verse": entity.verse.value,
                        "titre": entity.titre,
                        "profile": entity.profile,
                        "category": entity.category.value,
                        "region": region,
                        "department": department,
                        "limit_date": limit_date,
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

    def find_by_id(self, offer_id: int) -> Optional[Offer]:
        """Find an Offer by its ID."""
        try:
            offer_model = OfferModel.objects.get(id=offer_id)
            return offer_model.to_entity()
        except OfferModel.DoesNotExist:
            return None
