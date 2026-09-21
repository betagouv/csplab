from datetime import datetime, timezone
from time import time

import pytest
from faker import Faker

from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    CachedToken,
    TalentsoftOrganisationPayload,
)
from tests.factories.talentsoft_factories import (
    TalentsoftCodedObjectFactory,
    TalentsoftOfferFactory,
    TalentsoftOrganisationFactory,
)

fake = Faker()


@pytest.mark.parametrize(
    "delay,is_valid", [(100, True), (31, True), (30, False), (-100, False)]
)
def test_is_valid_cached_token(delay, is_valid):
    token = CachedToken(
        access_token=fake.uuid4(),
        token_type=fake.word().capitalize(),
        expires_at_epoch=time() + delay,
    )

    assert token.is_valid() == is_valid


def test_modification_date_defaults_to_now_when_null():
    before = datetime.now(timezone.utc)

    offer = TalentsoftOfferFactory.build(modificationDate=None)

    assert offer.modificationDate is not None
    modification_date = datetime.fromisoformat(
        offer.modificationDate.replace("Z", "+00:00")
    )
    after = datetime.now(timezone.utc)
    assert before <= modification_date <= after


def test_organisation_payload_merges_referentiel_and_detail():
    referentiel = TalentsoftCodedObjectFactory.build(
        code=12903, parentCode=12899, hasChildren=True
    )
    detail = TalentsoftOrganisationFactory.build()

    payload = TalentsoftOrganisationPayload.from_referentiel_and_detail(
        referentiel, detail
    )

    assert payload.code == 12903
    assert payload.parentCode == 12899
    assert payload.hasChildren is True
    assert payload.entityCode == detail.entityCode
    assert payload.name == detail.name


def test_organisation_payload_defaults_when_no_parent():
    referentiel = TalentsoftCodedObjectFactory.build(
        code=1, parentCode=None, hasChildren=False
    )
    detail = TalentsoftOrganisationFactory.build()

    payload = TalentsoftOrganisationPayload.from_referentiel_and_detail(
        referentiel, detail
    )

    assert payload.parentCode is None
    assert payload.hasChildren is False
