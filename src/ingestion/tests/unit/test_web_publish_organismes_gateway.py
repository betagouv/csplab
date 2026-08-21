import json
from datetime import date
from uuid import UUID, uuid4

import httpx
import pytest
from pytest_httpx import HTTPXMock
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.web_publish_organismes_gateway import (
    WebPublishOrganismesGateway,
)
from tests.conftest import PUBLISH_ORGANISMES_URL as PUBLISH_URL
from tests.conftest import WEB_API_KEY as API_KEY
from tests.conftest import WEB_BASE_URL as BASE_URL

ORGANISME_ID = UUID("11111111-2222-3333-4444-555555555555")

MINIMAL_ORGANISME = Organisme.build(
    entity_id=ORGANISME_ID,
    nom="Mairie de Test",
    versant=Verse.FPT,
    localisation=None,
    siret=SIRET(code="26060047300342"),
)

FULL_ORGANISME = Organisme.build(
    entity_id=uuid4(),
    nom="Hopital de Test",
    versant=Verse.FPH,
    localisation=Localisation(
        area=GeographicalArea.EUROPE,
        country=Country("FRA"),
        region=Region(code="11"),
        department=Department(code="75"),
        latitude=48.8566,
        longitude=2.3522,
    ),
    siret=SIRET(code="26060047300342"),
    parent_id=ORGANISME_ID,
    external_id="060786738",
    referentiel="FINESS",
    millesime="2026-08-19",
    gestion_ats=True,
    date_creation=date(2020, 1, 1),
    date_derniere_activite=date(2026, 1, 1),
)


@pytest.fixture
def gateway():
    client = httpx.AsyncClient()
    return WebPublishOrganismesGateway(
        client=client, base_url=BASE_URL, api_key=API_KEY
    )


@pytest.mark.asyncio
async def test_publish_posts_to_correct_url(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([MINIMAL_ORGANISME])

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].url == PUBLISH_URL


@pytest.mark.asyncio
async def test_publish_sends_api_key_header(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([MINIMAL_ORGANISME])

    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == f"Api-Key {API_KEY}"


@pytest.mark.asyncio
async def test_publish_serializes_minimal_organisme(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([MINIMAL_ORGANISME])

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert list(body.keys()) == ["organismes"]
    assert len(body["organismes"]) == 1
    organisme = body["organismes"][0]

    assert organisme["id"] == str(ORGANISME_ID)
    assert organisme["nom"] == "Mairie de Test"
    assert organisme["versant"] == "FPT"
    assert organisme["siret"] == "26060047300342"
    assert organisme["parent_id"] is None
    assert organisme["external_id"] is None
    assert organisme["referentiel"] is None
    assert organisme["millesime"] is None
    assert organisme["gestion_ats"] is False
    assert organisme["date_creation"] is None
    assert organisme["date_derniere_activite"] is None
    assert organisme["localisation"] is None


@pytest.mark.asyncio
async def test_publish_serializes_multiple_organismes(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([MINIMAL_ORGANISME, FULL_ORGANISME])

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert len(body["organismes"]) == 2


@pytest.mark.asyncio
async def test_publish_serializes_full_organisme(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish([FULL_ORGANISME])

    body = json.loads(httpx_mock.get_requests()[0].content)
    organisme = body["organismes"][0]

    assert organisme["versant"] == "FPH"
    assert organisme["parent_id"] == str(ORGANISME_ID)
    assert organisme["external_id"] == "060786738"
    assert organisme["referentiel"] == "FINESS"
    assert organisme["millesime"] == "2026-08-19"
    assert organisme["gestion_ats"] is True
    assert organisme["date_creation"] == "2020-01-01"
    assert organisme["date_derniere_activite"] == "2026-01-01"
    assert organisme["localisation"] == {
        "zone_geographique": "EU",
        "pays": "FRA",
        "region": "11",
        "departement": "75",
        "latitude": 48.8566,
        "longitude": 2.3522,
    }


@pytest.mark.asyncio
async def test_publish_raises_on_http_error(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=500)

    with pytest.raises(httpx.HTTPStatusError):
        await gateway.publish([MINIMAL_ORGANISME])


@pytest.mark.asyncio
async def test_publish_raises_and_logs_error_when_response_contains_errors(
    gateway, httpx_mock: HTTPXMock, caplog
):
    httpx_mock.add_response(
        method="POST",
        url=PUBLISH_URL,
        status_code=201,
        json={
            "created": 0,
            "updated": 0,
            "errors": [{"organisme": {"id": str(ORGANISME_ID)}, "error": "invalid"}],
        },
    )

    with caplog.at_level("ERROR"), pytest.raises(ExternalApiError):
        await gateway.publish([MINIMAL_ORGANISME])

    assert any("invalid" in record.getMessage() for record in caplog.records)


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
        await gateway.publish([MINIMAL_ORGANISME])

    assert caplog.records == []
