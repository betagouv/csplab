import logging
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from django.db import transaction
from django.utils import timezone
from pydantic import HttpUrl
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_criteria import OfferCriteria
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from application.ingestion.services.offer_references import format_reference
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
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


def build_offer(source_id: UUID, data: dict) -> PendingOffer:
    """Unsaved offer built from the validated payload of `creer_modifier`."""
    description = data["description"]
    profession = data["profession"]
    publication = data["publication"]
    conditions = data.get("conditions") or None
    debut_contrat = conditions.get("debut_contrat") if conditions else None
    criteria = OfferCriteria.from_dict(data.get("criteres"))
    application_url = data.get("url_candidature")

    offer = OfferModel(
        id=uuid4(),
        source_id=source_id,
        reference=data["identification"]["reference"],
        verse=Verse(data["identification"]["versant"]).value,
        title=data["titre"],
        long_title=data.get("titre_long") or None,
        profile=description["profil"],
        mission=description["mission"],
        employer=description.get("employeur") or None,
        complements=description.get("complements") or None,
        exercise_conditions=description.get("conditions_exercice") or None,
        service_description=description.get("descriptif_service") or None,
        organization=data["organisation"]["nom"],
        talentsoft_organisme_entity_code_id=data["organisation"].get(
            "talentsoft_organisme_entity_code"
        )
        or None,
        categories=[Category(category).value for category in data["categories"]],
        offer_nature=OfferNature(data["nature_offre"]).value,
        offer_url=data.get("url_offre") or None,
        code_emploi_csp=profession["metier"],
        job_family_referential=profession.get("referentiel"),
        local_job_code=profession.get("code_emploi_local"),
        functional_area_code=profession.get("domaine"),
        publication_date=publication["debut_publication"],
        end_publication_date=publication["fin_publication"],
        application_deadline=publication.get("fin_candidature"),
        job_vacancy_date=publication.get("debut_vacance_poste"),
        beginning_date=debut_contrat or None,
        application_url=str(HttpUrl(application_url)) if application_url else None,
        application_email=data.get("email_candidature"),
        contract_kind=data.get("type_contrat") or None,
        job_vacancy=data.get("vacance_poste") or None,
        criteria=criteria.to_dict() if criteria else None,
        conditions=conditions,
        contacts=list(data["contacts"]) if data.get("contacts") else None,
        archived_at=None,
    )
    return PendingOffer(
        offer=offer,
        localisations=[
            _localisation(localisation)
            for localisation in data.get("localisation") or []
            if localisation
        ],
    )


def _localisation(data: dict) -> Localisation:
    return Localisation(
        area=GeographicalArea(data["zone_geographique"]),
        country=Country(data["pays"]),
        region=Region(code=data["region"]) if data["region"] else None,
        department=(
            Department(code=data["departement"]) if data["departement"] else None
        ),
        label=data.get("localisation_label") or None,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )


def upsert_offers(
    source_id: UUID, pending_offers: list[PendingOffer], user: UserModel | None
) -> dict:
    """Create or update offers of a source, matched by reference.

    `user` is the JWT-authenticated user, who must be granted the source;
    `None` for the ingestion service, authenticated by API key.
    """
    if user is not None and not user.sources.filter(source_id=source_id).exists():
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
