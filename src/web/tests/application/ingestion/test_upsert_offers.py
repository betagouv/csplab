from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest
from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region

from application.ingestion.services.upsert_offers import PendingOffer, upsert_offers
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.authentication.api_key_authentication import (
    IngestionApiKeyUser,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

pytestmark = pytest.mark.django_db


def _pending(source, reference: str, localisations=None, **overrides):
    return PendingOffer(
        offer=OfferDjangoFactory.build(source=source, reference=reference, **overrides),
        localisations=localisations or [],
    )


def test_creates_new_offers_and_updates_existing_ones():
    existing = OfferDjangoFactory(title="Ancien titre")
    source_id = existing.source_id

    result = upsert_offers(
        source_id,
        [
            _pending(existing.source, existing.reference, title="Nouveau titre"),
            _pending(existing.source, "REF-NEW"),
        ],
        user=IngestionApiKeyUser(),
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
        Localisation(
            area=GeographicalArea.EUROPE,
            country=Country("FRA"),
            region=Region(code="28"),
            department=Department(code="14"),
            label="Caen",
        ),
        Localisation(
            area=GeographicalArea.AFRIQUE,
            country=Country("MAR"),
            region=None,
            department=None,
        ),
    ]

    upsert_offers(
        existing.source_id,
        [_pending(existing.source, existing.reference, localisations=localisations)],
        user=IngestionApiKeyUser(),
    )

    assert [
        (localisation.country, localisation.department, localisation.label)
        for localisation in existing.localisations.order_by("position")
    ] == [("FRA", "14", "Caen"), ("MAR", None, "")]


def test_moves_offer_to_the_organisme_sent_again():
    existing = OfferDjangoFactory(organisme=OrganismeDjangoFactory())
    other_organisme = OrganismeDjangoFactory()

    upsert_offers(
        existing.source_id,
        [_pending(existing.source, existing.reference, organisme=other_organisme)],
        user=IngestionApiKeyUser(),
    )

    existing.refresh_from_db()
    assert existing.organisme_id == other_organisme.id


def test_detaches_offer_sent_again_with_a_talentsoft_organisme():
    existing = OfferDjangoFactory(organisme=OrganismeDjangoFactory())
    talentsoft_organisme = TalentsoftOrganismeDjangoFactory()

    upsert_offers(
        existing.source_id,
        [
            _pending(
                existing.source,
                existing.reference,
                talentsoft_organisme_entity_code=talentsoft_organisme,
            )
        ],
        user=IngestionApiKeyUser(),
    )

    existing.refresh_from_db()
    assert existing.organisme_id is None
    assert existing.talentsoft_organisme_entity_code_id == (
        talentsoft_organisme.entity_code
    )


def test_unarchives_offer_and_makes_it_eligible_for_reindexing():
    archived = OfferDjangoFactory(
        archived_at=datetime.now(timezone.utc),
        processed_at=datetime.now(timezone.utc) - relativedelta(days=1),
        updated_at=datetime.now(timezone.utc) - relativedelta(days=1),
    )

    upsert_offers(
        archived.source_id,
        [_pending(archived.source, archived.reference)],
        user=IngestionApiKeyUser(),
    )

    archived.refresh_from_db()
    assert archived.archived_at is None
    assert archived.updated_at > archived.processed_at


def test_generates_auto_references():
    source = OfferDjangoFactory().source

    result = upsert_offers(
        source.source_id,
        [
            _pending(source, "auto"),
            _pending(source, "REF-1"),
            _pending(source, "auto", title="Troisième"),
        ],
        user=IngestionApiKeyUser(),
    )

    year = datetime.now(ZoneInfo("Europe/Paris")).year
    assert result["offres"] == [
        {"reference": f"CSP-{year}-000001", "statut": "created"},
        {"reference": "REF-1", "statut": "created"},
        {"reference": f"CSP-{year}-000002", "statut": "created"},
    ]
    assert not OfferModel.objects.filter(reference="auto").exists()
    assert OfferModel.objects.get(reference=f"CSP-{year}-000002").title == ("Troisième")


def test_database_error_rolls_back_the_whole_batch():
    source = SourceDjangoFactory()

    with pytest.raises(IntegrityError):
        upsert_offers(
            source.source_id,
            [
                _pending(source, "REF-1"),
                _pending(source, "REF-2"),
                _pending(source, "REF-1"),
            ],
            user=IngestionApiKeyUser(),
        )

    assert not OfferModel.objects.exists()


def test_user_without_the_source_is_refused(test_user):
    source = SourceDjangoFactory()

    with pytest.raises(SourceAuthorizationError):
        upsert_offers(source.source_id, [_pending(source, "REF-1")], user=test_user)

    assert not OfferModel.objects.exists()


def test_user_with_the_source_upserts(test_user):
    source = SourceDjangoFactory()
    test_user.sources.add(source)

    result = upsert_offers(
        source.source_id, [_pending(source, "REF-1")], user=test_user
    )

    assert result["created"] == 1
