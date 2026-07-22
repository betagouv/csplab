from datetime import datetime, timezone
from time import time

import pytest
from faker import Faker

from infrastructure.external_gateways.dtos.talentsoft_dtos import CachedToken
from tests.factories.talentsoft_factories import TalentsoftOfferFactory

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
