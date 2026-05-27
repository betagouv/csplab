import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from application.use_cases.archive_offer import ArchiveOfferUseCase
from tests.shared_fixtures import WEB_API_KEY, WEB_BASE_URL

REFERENCE = "2019-1234"
SOURCE_ID = "talentsoft-client-1"
ARCHIVE_URL = f"{WEB_BASE_URL}/api/v1/offres/archiver"


@pytest.mark.asyncio
async def test_execute_posts_to_archive_endpoint(
    archive_offer_use_case: ArchiveOfferUseCase, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=ARCHIVE_URL, status_code=200)
    await archive_offer_use_case.execute(REFERENCE, source_id=SOURCE_ID)

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].url == httpx.URL(ARCHIVE_URL)
    assert requests[0].headers["authorization"] == f"Api-Key {WEB_API_KEY}"
    body = json.loads(requests[0].content)
    assert body == {"reference": REFERENCE, "source_id": SOURCE_ID}


@pytest.mark.asyncio
async def test_execute_raises_on_error_response(
    archive_offer_use_case: ArchiveOfferUseCase, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=ARCHIVE_URL, status_code=500)
    with pytest.raises(httpx.HTTPStatusError):
        await archive_offer_use_case.execute(REFERENCE, source_id=SOURCE_ID)
