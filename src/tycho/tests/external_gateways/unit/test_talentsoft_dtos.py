"""Unit tests for Talentsoft DTOs."""

from time import time

import pytest
from faker import Faker

from infrastructure.external_gateways.dtos.talentsoft_dtos import CachedToken

fake = Faker()


@pytest.mark.parametrize(
    "delay,is_valid", [(100, True), (31, True), (30, False), (-100, False)]
)
def test_is_valid_cached_token(delay, is_valid):
    """Test that token is valid depending of expiry."""
    token = CachedToken(
        access_token=fake.uuid4(),
        token_type=fake.word().capitalize(),
        expires_at_epoch=time() + delay,
    )

    assert token.is_valid() == is_valid
