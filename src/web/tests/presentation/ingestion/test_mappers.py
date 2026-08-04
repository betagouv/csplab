from datetime import datetime, timezone
from uuid import uuid4

import pytest

from infrastructure.factories.ingestion.offer_payload_factory import PayloadOfferFactory
from presentation.ingestion.mappers import OfferInputMapper, OfferSummaryOutputMapper


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, None),
        (datetime(2024, 1, 15, tzinfo=timezone.utc), "2024-01-15T00:00:00"),
        (
            datetime(2026, 7, 30, 10, 8, 39, 230000, tzinfo=timezone.utc),
            "2026-07-30T10:08:39.23",
        ),
    ],
    ids=[
        "none-value-returns-none",
        "no-microsecond-has-no-fractional-part",
        "microsecond-truncated-to-centiseconds-and-drops-timezone",
    ],
)
def test_isoformat(value, expected):
    assert OfferSummaryOutputMapper._isoformat(value) == expected


def test_offer_input_mapper_maps_profession_referentiel_to_job_family_referential():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        profession={"domaine": "NUM", "metier": "ERNUM001", "referentiel": "RMFPv2"},
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.job_family_referential == "RMFPv2"


def test_offer_input_mapper_maps_profession_domaine_to_functional_area_code():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        profession={"domaine": "NUM", "metier": "ERNUM001", "referentiel": "RMFPv2"},
    )

    offer = OfferInputMapper().to_domain(payload, source_id=uuid4())

    assert offer.functional_area_code == "NUM"
