"""Django implementation of IOffersRepository."""

from typing import Dict, List

from domain.entities.offer import Offer
from domain.exceptions.offer_errors import OfferDoesNotExist
from domain.repositories.document_repository_interface import (
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

        try:
            # Get existing external_ids in one query
            existing_external_ids = set(
                OfferModel.objects.filter(
                    external_id__in=[offer.external_id for offer in offers_list]
                ).values_list("external_id", flat=True)
            )

            # Partition offers into new and existing
            partitioned: Dict[str, List[Offer]] = {"new": [], "existing": []}
            for offer in offers_list:
                if offer.external_id in existing_external_ids:
                    partitioned["existing"].append(offer)
                else:
                    partitioned["new"].append(offer)

            created = 0
            updated = 0

            # Bulk create new offers
            if partitioned["new"]:
                new_models = [
                    OfferModel.from_entity(offer) for offer in partitioned["new"]
                ]
                OfferModel.objects.bulk_create(new_models, ignore_conflicts=True)
                created = len(new_models)

            # Bulk update existing offers
            if partitioned["existing"]:
                # Get existing models to update
                existing_models = list(
                    OfferModel.objects.filter(
                        external_id__in=[
                            offer.external_id for offer in partitioned["existing"]
                        ]
                    )
                )

                # Create mapping for efficient lookup
                existing_models_map = {
                    model.external_id: model for model in existing_models
                }

                # Update models using from_entity
                models_to_update = []
                for offer in partitioned["existing"]:
                    if offer.external_id in existing_models_map:
                        existing_model = existing_models_map[offer.external_id]
                        updated_model = OfferModel.from_entity(offer)
                        # Keep the existing ID and timestamps
                        updated_model.id = existing_model.id
                        updated_model.created_at = existing_model.created_at
                        models_to_update.append(updated_model)

                if models_to_update:
                    OfferModel.objects.bulk_update(
                        models_to_update,
                        fields=[
                            "verse",
                            "title",
                            "profile",
                            "mission",
                            "category",
                            "contract_type",
                            "organization",
                            "offer_url",
                            "country",
                            "region",
                            "department",
                            "publication_date",
                            "beginning_date",
                        ],
                    )
                    updated = len(models_to_update)

            return {"created": created, "updated": updated, "errors": []}

        except Exception as e:
            db_error = DatabaseError(
                f"Erreur lors de l'upsert batch des offres: {str(e)}"
            )
            return {
                "created": 0,
                "updated": 0,
                "errors": [
                    {
                        "entity_id": None,
                        "error": f"Database error during bulk upsert: {str(e)}",
                        "exception": db_error,
                    }
                ],
            }

    def find_by_id(self, offer_id: int) -> Offer:
        """Find an Offer by its ID."""
        try:
            offer_model = OfferModel.objects.get(id=offer_id)
            return offer_model.to_entity()
        except OfferModel.DoesNotExist as e:
            raise OfferDoesNotExist(offer_id) from e
