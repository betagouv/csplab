"""Utils for tests using external gateways."""

from time import time
from typing import Any, Dict, Optional
from unittest.mock import Mock

from faker import Faker
from httpx import Response

from domain.types import JsonDataType
from infrastructure.external_gateways.dtos.talentsoft_dtos import CachedToken
from tests.fixtures.fixture_loader import load_fixture

fake = Faker()


def _load_offer_fixture_data(doc_id: int) -> Dict[str, Any]:
    """Load and return offer fixture data for given doc_id."""
    offer_fixtures = load_fixture("offers_talentsoft_20260124.json")
    fixture_index = (doc_id - 1) % len(offer_fixtures)
    return offer_fixtures[fixture_index].copy()


def cached_token(access_token: Optional[str] = None, expire_in: int = 3600):
    """Create a cached token."""
    return CachedToken(
        access_token=fake.uuid4() if access_token is None else access_token,
        token_type=fake.word().capitalize(),
        expires_at_epoch=time() + expire_in,
        refresh_token=fake.uuid4(),
    )


def offers_response(count: int = 2, has_more: bool = False):
    """Create offers response."""
    offers = [_load_offer_fixture_data(i) for i in range(1, count + 1)]

    offers_response = {
        "data": offers,
        "_pagination": {
            "start": 1,
            "count": count,
            "total": count + (10 if has_more else 0),
            "resultsPerPage": count,
            "hasMore": has_more,
            "lastPage": 1 if not has_more else 2,
        },
    }
    return offers_response


def mocked_response(status_code: int = 200, return_value: JsonDataType = None):
    """Create a mocked response."""
    response = Mock(spec=Response)
    response.status_code = status_code
    response.json.return_value = return_value
    response.raise_for_status = Mock(return_value=None)
    return response
