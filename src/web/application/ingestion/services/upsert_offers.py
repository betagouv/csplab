import logging
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from django.db import transaction
from django.utils import timezone
from referentiel.value_objects.localisation import Localisation

from application.ingestion.services.offer_references import format_reference
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.authentication.api_key_authentication import (
    IngestionApiKeyUser,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.referentiel.models.offer_localisation import (
    OfferLocalisationModel,
)
from infrastructure.django_apps.referentiel.models.offer_reference_sequence import (
    OfferReferenceSequenceModel,
)
from infrastructure.django_apps.users.models import UserModel

logger = logging.getLogger(__name__)

AUTO_REFERENCE = "auto"
TIMEZONE = ZoneInfo("Europe/Paris")

UPDATE_FIELDS = [
    "reference",
    "verse",
    "title",
    "profile",
    "mission",
    "categories",
    "offer_nature",
    "organization",
    "offer_url",
    "code_emploi_csp",
    "job_family_referential",
    "local_job_code",
    "functional_area_code",
    "publication_date",
    "end_publication_date",
    "beginning_date",
    "application_deadline",
    "job_vacancy_date",
    "updated_at",
    "archived_at",
    "long_title",
    "application_url",
    "application_email",
    "contract_kind",
    "job_vacancy",
    "employer",
    "complements",
    "exercise_conditions",
    "service_description",
    "criteria",
    "conditions",
    "contacts",
    "talentsoft_organisme_entity_code",
]


@dataclass
class PendingOffer:
    offer: OfferModel
    localisations: list[Localisation] = field(default_factory=list)


def upsert_offers(
    source_id: UUID,
    pending_offers: list[PendingOffer],
    user: UserModel | IngestionApiKeyUser,
) -> dict:
    if (
        not isinstance(user, IngestionApiKeyUser)
        and not user.sources.filter(source_id=source_id).exists()
    ):
        raise SourceAuthorizationError({source_id})
    if not pending_offers:
        return {"created": 0, "updated": 0, "offres": []}

    _generate_auto_references([pending.offer for pending in pending_offers])
    logger.info("upsert_offers: upserting %d offers", len(pending_offers))

    with transaction.atomic():
        existing_ids = dict(
            OfferModel.objects.by_source(source_id)
            .by_references({pending.offer.reference for pending in pending_offers})
            .select_for_update(of=("self",))
            .values_list("reference", "id")
        )
        new_offers = []
        updated_offers = []
        for pending in pending_offers:
            offer = pending.offer
            if offer.reference in existing_ids:
                offer.id = existing_ids[offer.reference]
                offer.updated_at = timezone.now()
                updated_offers.append(offer)
            else:
                new_offers.append(offer)

        created = len(OfferModel.objects.bulk_create(new_offers))
        updated = (
            OfferModel.objects.bulk_update(updated_offers, fields=UPDATE_FIELDS)
            if updated_offers
            else 0
        )

        OfferLocalisationModel.objects.filter(
            offer_id__in=[pending.offer.id for pending in pending_offers]
        ).delete()
        OfferLocalisationModel.objects.bulk_create(
            OfferLocalisationModel.from_localisation(
                pending.offer.id, position, localisation
            )
            for pending in pending_offers
            for position, localisation in enumerate(pending.localisations)
        )

    logger.info("upsert_offers: created=%d updated=%d", created, updated)
    return {
        "created": created,
        "updated": updated,
        "offres": [
            {
                "reference": pending.offer.reference,
                "statut": "updated"
                if pending.offer.reference in existing_ids
                else "created",
            }
            for pending in pending_offers
        ],
    }


def _generate_auto_references(offers: list[OfferModel]) -> None:
    auto_offers = [offer for offer in offers if offer.reference == AUTO_REFERENCE]
    if not auto_offers:
        return
    year = datetime.now(TIMEZONE).year
    numbers = OfferReferenceSequenceModel.objects.reserve(
        year=year, count=len(auto_offers)
    )
    for offer, number in zip(auto_offers, numbers, strict=True):
        offer.reference = format_reference(year, number)
