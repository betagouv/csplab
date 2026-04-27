from time import time
from typing import Any, Dict, List, Optional
from unittest.mock import Mock

from faker import Faker
from httpx import Response

from domain.types import JsonDataType
from infrastructure.external_gateways.dtos.talentsoft_dtos import CachedToken
from tests.factories.talentsoft_factories import (
    TalentsoftDetailOfferFactory,
    TalentsoftOfferFactory,
)

fake = Faker()


def _build_offer_data() -> Dict[str, Any]:
    return TalentsoftOfferFactory.build().model_dump()


def cached_token(access_token: Optional[str] = None, expire_in: int = 3600):
    return CachedToken(
        access_token=fake.uuid4() if access_token is None else access_token,
        token_type=fake.word().capitalize(),
        expires_at_epoch=time() + expire_in,
        refresh_token=fake.uuid4(),
    )


def offers_response(
    count: int = 2, has_more: bool = False, offers: List[Any] | None = None
):
    if not offers:
        offers = [_build_offer_data() for _ in range(count)]

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


def detail_offer_response(reference: Optional[str] = None) -> Dict[str, Any]:
    offer = TalentsoftDetailOfferFactory.build()
    data = offer.model_dump()
    data["reference"] = reference if reference is not None else fake.uuid4()
    return data


def mocked_response(status_code: int = 200, return_value: JsonDataType = None):
    response = Mock(spec=Response)
    response.status_code = status_code
    response.json.return_value = return_value
    response.raise_for_status = Mock(return_value=None)
    return response
