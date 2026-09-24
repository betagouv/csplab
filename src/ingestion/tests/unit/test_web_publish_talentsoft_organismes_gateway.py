import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from infrastructure.external_gateways.base_web_gateway import WebGatewayCredentials
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftGeolocation,
    TalentsoftOrganisationPayload,
)
from infrastructure.external_gateways.web_publish_talentsoft_organismes_gateway import (
    WebPublishTalentsoftOrganismesGateway,
)
from tests.conftest import PUBLISH_TALENTSOFT_ORGANISMES_URL as PUBLISH_URL
from tests.conftest import WEB_API_KEY as API_KEY
from tests.conftest import WEB_BASE_URL as BASE_URL


def _organisation(**overrides) -> TalentsoftOrganisationPayload:
    defaults = {"entityCode": "123", "name": "Mairie de Test", "code": 123}
    defaults.update(overrides)
    return TalentsoftOrganisationPayload(**defaults)


@pytest.fixture
def gateway():
    client = httpx.AsyncClient()
    return WebPublishTalentsoftOrganismesGateway(
        client=client,
        credentials=WebGatewayCredentials(base_url=BASE_URL, api_key=API_KEY),
    )


@pytest.mark.asyncio
async def test_publish_posts_to_correct_url(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([_organisation()])

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].url == PUBLISH_URL


@pytest.mark.asyncio
async def test_publish_sends_api_key_header(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([_organisation()])

    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == f"Api-Key {API_KEY}"


@pytest.mark.asyncio
async def test_publish_serializes_minimal_organisation(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([_organisation(entityCode="123", name="Mairie de Test")])

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert list(body.keys()) == ["talentsoft_organismes"]
    assert len(body["talentsoft_organismes"]) == 1
    item = body["talentsoft_organismes"][0]
    assert item["entity_code"] == "123"
    assert item["name"] == "Mairie de Test"
    assert "organisme_id" not in item


@pytest.mark.asyncio
async def test_publish_serializes_geolocation(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    organisation = _organisation(
        geolocation=TalentsoftGeolocation(latitude=48.85, longitude=2.35)
    )

    await gateway.publish([organisation])

    body = json.loads(httpx_mock.get_requests()[0].content)
    item = body["talentsoft_organismes"][0]
    assert item["latitude"] == 48.85
    assert item["longitude"] == 2.35


@pytest.mark.asyncio
async def test_publish_serializes_code_as_string(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    organisation = _organisation(code=7060)

    await gateway.publish([organisation])

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["talentsoft_organismes"][0]["code"] == "7060"


@pytest.mark.asyncio
async def test_publish_serializes_parent_code_as_string(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    organisation = _organisation(parentCode=456)

    await gateway.publish([organisation])

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["talentsoft_organismes"][0]["parent_code"] == "456"


@pytest.mark.asyncio
async def test_publish_batches_all_organisations_in_one_request(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    organisations = [
        _organisation(entityCode=str(code), code=code) for code in range(5)
    ]

    await gateway.publish(organisations)

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert len(body["talentsoft_organismes"]) == 5


@pytest.mark.asyncio
async def test_publish_raises_on_http_error(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=500)

    with pytest.raises(httpx.HTTPStatusError):
        await gateway.publish([_organisation()])


@pytest.mark.asyncio
async def test_publish_logs_error_when_response_contains_errors(
    gateway, httpx_mock: HTTPXMock, caplog
):
    httpx_mock.add_response(
        method="POST",
        url=PUBLISH_URL,
        status_code=201,
        json={
            "created": 0,
            "updated": 0,
            "errors": [
                {
                    "talentsoft_organisme": {
                        "entity_code": "123",
                        "organisme_id": None,
                    },
                    "error": "Organisme introuvable.",
                }
            ],
        },
    )

    with caplog.at_level("ERROR"):
        await gateway.publish([_organisation()])

    assert any("123" in record.getMessage() for record in caplog.records)


@pytest.mark.asyncio
async def test_publish_does_not_log_when_response_has_no_errors(
    gateway, httpx_mock: HTTPXMock, caplog
):
    httpx_mock.add_response(
        method="POST",
        url=PUBLISH_URL,
        status_code=201,
        json={"created": 1, "updated": 0, "errors": []},
    )

    with caplog.at_level("ERROR"):
        await gateway.publish([_organisation()])

    assert caplog.records == []
