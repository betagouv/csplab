"""Utils for tests using external gateways."""

from time import time
from typing import Optional
from unittest.mock import Mock

from faker import Faker
from httpx import Response

from domain.types import JsonDataType
from infrastructure.external_gateways.dtos.talentsoft_dtos import CachedToken

fake = Faker()


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
    offers = [
        {
            "reference": fake.uuid4(),
            "title": fake.job(),
            "salaryRange": {"clientCode": fake.word()},
        }
        for i in range(count)
    ]
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
