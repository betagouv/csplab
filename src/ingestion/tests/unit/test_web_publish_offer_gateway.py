import json
from datetime import datetime, timezone
from uuid import UUID

import httpx
import pytest
from pytest_httpx import HTTPXMock

from domain.entities.offer import Offer
from domain.value_objects.area import GeographicalArea
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse
from infrastructure.external_gateways.web_publish_offer_gateway import (
    WebPublishOfferGateway,
)

BASE_URL = "https://web.example.com"
API_KEY = "test-api-key"
PUBLISH_URL = f"{BASE_URL}/api/v1/offres/creer_modifier/"
SOURCE_ID = str(UUID("11111111-2222-3333-4444-555555555555"))
PUBLICATION_DATE = datetime(2024, 1, 15, tzinfo=timezone.utc)

MINIMAL_OFFER = Offer(
    reference="2024-OFFER-001",
    source_id=SOURCE_ID,
    external_id="FPT-2024-OFFER-001",
    title="Software Engineer",
    profile="Profile text",
    mission="Mission text",
    organization="City Hall",
    verse=Verse.FPT,
    category=None,
    contract_type=ContractType.TITULAIRE_CONTRACTUEL,
    offer_url=None,
    localisation=None,
    publication_date=PUBLICATION_DATE,
    beginning_date=None,
    family_code="INF001",
)

FULL_OFFER = Offer(
    reference="2024-OFFER-002",
    source_id=SOURCE_ID,
    external_id="FPH-2024-OFFER-002",
    title="Nurse Manager",
    profile="Profile text",
    mission="Mission text",
    organization="Hospital",
    verse=Verse.FPH,
    category=Category.A,
    contract_type=ContractType.CONTRACTUELS,
    offer_url=None,
    localisation=Localisation(
        area=GeographicalArea.EUROPE,
        country=Country("FRA"),
        region=Region(code="11"),
        department=Department(code="75"),
    ),
    publication_date=PUBLICATION_DATE,
    beginning_date=LimitDate(value=datetime(2024, 6, 1, tzinfo=timezone.utc)),
    family_code="MED001",
)


@pytest.fixture
def gateway():
    client = httpx.AsyncClient()
    return WebPublishOfferGateway(client=client, base_url=BASE_URL, api_key=API_KEY)


@pytest.mark.asyncio
async def test_publish_posts_to_correct_url(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(MINIMAL_OFFER)

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].url == PUBLISH_URL


@pytest.mark.asyncio
async def test_publish_sends_api_key_header(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(MINIMAL_OFFER)

    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == f"Api-Key {API_KEY}"


@pytest.mark.asyncio
async def test_publish_serializes_minimal_offer(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(MINIMAL_OFFER)

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert list(body.keys()) == ["offres"]
    assert len(body["offres"]) == 1
    offer = body["offres"][0]

    assert offer["identification"]["reference"] == "2024-OFFER-001"
    assert offer["identification"]["source"] == str(SOURCE_ID)
    assert offer["identification"]["versant"] == "FPT"
    assert offer["titre"] == "Software Engineer"
    assert offer["titre_long"] == "Software Engineer"
    assert offer["organisation"]["nom"] == "City Hall"
    assert offer["organisation"]["siret"] == ""
    assert offer["url_offre"] is None
    assert offer["url_candidature"] is None
    assert offer["profession"]["domaine"] == "INF"
    assert offer["profession"]["metier"] == "INF001"
    assert offer["categories"] == []
    assert offer["type_contrat"] == "TITULAIRE_CONTRACTUEL"
    assert offer["forme_contrat"] == []
    assert offer["vacance_poste"] == ""
    assert offer["description"]["mission"] == "Mission text"
    assert offer["description"]["profil"] == "Profile text"
    assert offer["description"]["employeur"] == "City Hall"
    assert offer["description"]["complements"] == ""
    assert offer["localisation"] is None
    assert offer["criteres"] is None
    assert offer["conditions"] is None
    assert offer["contacts"] is None
    assert offer["publication"]["debut_publication"] == "2024-01-15T00:00:00Z"


@pytest.mark.asyncio
async def test_publish_uses_beginning_date_as_fin_publication(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(FULL_OFFER)

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["publication"]["fin_publication"] == "2024-06-01T00:00:00Z"


@pytest.mark.asyncio
async def test_publish_defaults_fin_publication_to_one_year_when_no_beginning_date(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(MINIMAL_OFFER)

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["publication"]["fin_publication"] == "2025-01-14T00:00:00Z"


@pytest.mark.asyncio
async def test_publish_serializes_localisation(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(FULL_OFFER)

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["localisation"] == [
        {
            "zone_geographique": "EU",
            "pays": "FRA",
            "region": "11",
            "departement": "75",
            "localisation_label": "",
            "latitude": None,
            "longitude": None,
        }
    ]


@pytest.mark.asyncio
async def test_publish_serializes_category(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(FULL_OFFER)

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["categories"] == ["A"]


@pytest.mark.asyncio
async def test_publish_raises_on_http_error(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=500)

    with pytest.raises(httpx.HTTPStatusError):
        await gateway.publish(MINIMAL_OFFER)
