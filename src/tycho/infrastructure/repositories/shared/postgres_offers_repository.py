"""Django implementation of IOffersRepository."""

from typing import List

from domain.entities.offer import Offer
from domain.exceptions.offer_errors import OfferDoesNotExist
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.repositories.offers_repository_interface import IOffersRepository
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.exceptions.exceptions import DatabaseError


class PostgresOffersRepository(IOffersRepository):
    """Django ORM implementation of IOffersRepository."""

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offer entities and return operation results."""
        if not offers_list:
            return {"created": 0, "updated": 0, "errors": []}

        errors: List[IUpsertError] = []

        try:
            # Get existing external_ids in one query
            existing_external_ids = set(
                OfferModel.objects.filter(
                    external_id__in=[offer.external_id for offer in offers_list]
                ).values_list("external_id", flat=True)
            )

            # Separate new and existing offers
            to_create = []
            to_update = []
            valid_offers = []

            for offer in offers_list:
                offer_model = OfferModel.from_entity(offer)
                valid_offers.append(offer)
                if offer.external_id in existing_external_ids:
                    to_update.append(offer_model)
                else:
                    to_create.append(offer_model)

            created = 0
            updated = 0

            # Bulk create new offers
            if to_create:
                try:
                    OfferModel.objects.bulk_create(to_create, ignore_conflicts=True)
                    created = len(to_create)
                except Exception as e:
                    # Add all failed creates to errors
                    for _, offer in enumerate(
                        [
                            o
                            for o in valid_offers
                            if o.external_id not in existing_external_ids
                        ]
                    ):
                        errors.append(
                            {
                                "entity_id": offer.id,
                                "error": f"Bulk create failed: {str(e)}",
                                "exception": e,
                            }
                        )

            # Bulk update existing offers
            if to_update:
                try:
                    OfferModel.objects.bulk_update(
                        to_update,
                        fields=[
                            "verse",
                            "title",
                            "profile",
                            "category",
                            "region",
                            "department",
                            "limit_date",
                        ],
                    )
                    updated = len(to_update)
                except Exception as e:
                    # Add all failed updates to errors
                    for offer in [
                        o
                        for o in valid_offers
                        if o.external_id in existing_external_ids
                    ]:
                        errors.append(
                            {
                                "entity_id": offer.id,
                                "error": f"Bulk update failed: {str(e)}",
                                "exception": e,
                            }
                        )

            return {"created": created, "updated": updated, "errors": errors}

        except Exception as e:
            raise DatabaseError("Erreur lors de l'upsert batch des offres") from e

    def find_by_id(self, offer_id: int) -> Offer:
        """Find an Offer by its ID."""
        try:
            offer_model = OfferModel.objects.get(id=offer_id)
            return offer_model.to_entity()
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(offer_id) from e
