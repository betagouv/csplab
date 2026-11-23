from datetime import datetime, timezone
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from dateutil.relativedelta import relativedelta

from application.ingestion.services.upsert_offers import build_offer, upsert_offers
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.ingestion.offer_payload_factory import PayloadOfferFactory
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

pytestmark = pytest.mark.django_db


def _pending(source_id: UUID, reference: str, **overrides):
    payload = PayloadOfferFactory.create(
        identification={"reference": reference, "versant": "FPT"}, **overrides
    )
    return build_offer(source_id, payload)


def test_creates_new_offers_and_updates_existing_ones():
    existing = OfferDjangoFactory(title="Ancien titre")
    source_id = existing.source_id

    result = upsert_offers(
        source_id,
        [
            _pending(source_id, existing.reference, titre="Nouveau titre"),
            _pending(source_id, "REF-NEW"),
        ],
        user=None,
    )

    assert result == {
        "created": 1,
        "updated": 1,
        "offres": [
            {"reference": existing.reference, "statut": "updated"},
            {"reference": "REF-NEW", "statut": "created"},
        ],
    }
    existing.refresh_from_db()
    assert existing.title == "Nouveau titre"
    assert set(
        OfferModel.objects.filter(source_id=source_id).values_list(
            "reference", flat=True
        )
    ) == {existing.reference, "REF-NEW"}


def test_localisations_are_replaced_in_sent_order():
    existing = OfferDjangoFactory(country="FRA", region="11", department="75")
    localisations = [
        {
            "zone_geographique": "EU",
            "pays": "FRA",
            "region": "28",
            "departement": "14",
            "localisation_label": "Caen",
            "latitude": None,
            "longitude": None,
        },
        {
            "zone_geographique": "AF",
            "pays": "MAR",
            "region": None,
            "departement": None,
            "localisation_label": "",
            "latitude": None,
            "longitude": None,
        },
    ]

    upsert_offers(
        existing.source_id,
        [_pending(existing.source_id, existing.reference, localisation=localisations)],
        user=None,
    )

    assert [
        (localisation.country, localisation.department, localisation.label)
        for localisation in existing.localisations.order_by("position")
    ] == [("FRA", "14", "Caen"), ("MAR", None, "")]


def test_unarchives_offer_and_makes_it_eligible_for_reindexing():
    archived = OfferDjangoFactory(
        archived_at=datetime.now(timezone.utc),
        processed_at=datetime.now(timezone.utc) - relativedelta(days=1),
        updated_at=datetime.now(timezone.utc) - relativedelta(days=1),
    )

    upsert_offers(
        archived.source_id,
        [_pending(archived.source_id, archived.reference)],
        user=None,
    )

    archived.refresh_from_db()
    assert archived.archived_at is None
    assert archived.updated_at > archived.processed_at


def test_generates_auto_references():
    source_id = OfferDjangoFactory().source_id

    result = upsert_offers(
        source_id,
        [
            _pending(source_id, "auto"),
            _pending(source_id, "REF-1"),
            _pending(source_id, "auto", titre="Troisième"),
        ],
        user=None,
    )

    year = datetime.now(ZoneInfo("Europe/Paris")).year
    assert result["offres"] == [
        {"reference": f"CSP-{year}-000001", "statut": "created"},
        {"reference": "REF-1", "statut": "created"},
        {"reference": f"CSP-{year}-000002", "statut": "created"},
    ]
    assert not OfferModel.objects.filter(reference="auto").exists()
    assert OfferModel.objects.get(reference=f"CSP-{year}-000002").title == ("Troisième")


def test_user_without_the_source_is_refused(test_user):
    source = SourceDjangoFactory()

    with pytest.raises(SourceAuthorizationError):
        upsert_offers(
            source.source_id, [_pending(source.source_id, "REF-1")], user=test_user
        )

    assert not OfferModel.objects.exists()


def test_user_with_the_source_upserts(test_user):
    source = SourceDjangoFactory()
    test_user.sources.add(source)

    result = upsert_offers(
        source.source_id, [_pending(source.source_id, "REF-1")], user=test_user
    )

    assert result["created"] == 1
