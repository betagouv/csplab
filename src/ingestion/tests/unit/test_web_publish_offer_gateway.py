import json
from datetime import datetime, timezone
from uuid import UUID

import httpx
import pytest
from pydantic import HttpUrl
from pytest_httpx import HTTPXMock
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language import Language
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.entities.offer import Offer
from domain.gateways.publish_offer_input import PublishOfferInput
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.web_publish_offer_gateway import (
    WebPublishOfferGateway,
)
from tests.conftest import PUBLISH_OFFER_URL as PUBLISH_URL
from tests.conftest import WEB_API_KEY as API_KEY
from tests.conftest import WEB_BASE_URL as BASE_URL

SOURCE_ID = UUID("11111111-2222-3333-4444-555555555555")
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
    application_url=None,
    localisation=None,
    publication_date=PUBLICATION_DATE,
    end_publication_date=None,
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
    application_url=None,
    localisation=Localisation(
        area=GeographicalArea.EUROPE,
        country=Country("FRA"),
        region=Region(code="11"),
        department=Department(code="75"),
    ),
    publication_date=PUBLICATION_DATE,
    end_publication_date=None,
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

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER))

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].url == PUBLISH_URL


@pytest.mark.asyncio
async def test_publish_sends_api_key_header(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER))

    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == f"Api-Key {API_KEY}"


@pytest.mark.asyncio
async def test_publish_serializes_minimal_offer(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert list(body.keys()) == ["source_id", "offres"]
    assert body["source_id"] == str(SOURCE_ID)
    assert len(body["offres"]) == 1
    offer = body["offres"][0]

    assert offer["identification"]["reference"] == "2024-OFFER-001"
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
async def test_publish_serializes_contract_kind(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    offer = Offer(**{**MINIMAL_OFFER.__dict__, "contract_kind": ContractKind.CDD})

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["forme_contrat"] == ["CDD"]


@pytest.mark.asyncio
async def test_publish_uses_end_publication_date_as_fin_publication(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    offer = Offer(
        **{
            **MINIMAL_OFFER.__dict__,
            "end_publication_date": datetime(2025, 3, 31, tzinfo=timezone.utc),
        }
    )

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["publication"]["fin_publication"] == "2025-03-31T00:00:00Z"


@pytest.mark.asyncio
async def test_publish_uses_beginning_date_as_fin_publication(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=FULL_OFFER))

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["publication"]["fin_publication"] == "2024-06-01T00:00:00Z"


@pytest.mark.asyncio
async def test_publish_defaults_fin_publication_to_one_year_when_no_beginning_date(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER))

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["publication"]["fin_publication"] == "2025-01-14T00:00:00Z"


@pytest.mark.asyncio
async def test_publish_serializes_localisation(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=FULL_OFFER))

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

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=FULL_OFFER))

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["categories"] == ["A"]


@pytest.mark.asyncio
async def test_publish_serializes_application_url(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    offer_with_app_url = Offer(
        **{
            **MINIMAL_OFFER.__dict__,
            "application_url": HttpUrl("https://apply.example.com/job/123"),
        }
    )

    await gateway.publish(
        PublishOfferInput(source_id=SOURCE_ID, offer=offer_with_app_url)
    )

    body = json.loads(httpx_mock.get_requests()[0].content)
    offer = body["offres"][0]
    assert offer["url_candidature"] == "https://apply.example.com/job/123"


@pytest.mark.asyncio
async def test_publish_serializes_criteres_with_education_level(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    offer = Offer(**{**MINIMAL_OFFER.__dict__, "education_level": 5})

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["criteres"] == {"diplome_niveau": 5}


@pytest.mark.asyncio
async def test_publish_serializes_criteres_with_experience(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    offer = Offer(**{**MINIMAL_OFFER.__dict__, "experience": ExperienceLevel.CONFIRME})

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["criteres"] == {"experience": "CONFIRME"}


@pytest.mark.asyncio
async def test_publish_serializes_criteres_with_diploma(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    offer = Offer(**{**MINIMAL_OFFER.__dict__, "diploma": "LICENCE"})

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["criteres"] == {"diplome": "LICENCE"}


@pytest.mark.asyncio
async def test_publish_serializes_criteres_with_specialisations(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)
    offer = Offer(**{**MINIMAL_OFFER.__dict__, "specialisations": ["SPEC_A", "SPEC_B"]})

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["criteres"] == {"specialisations": ["SPEC_A", "SPEC_B"]}


@pytest.mark.asyncio
async def test_publish_serializes_criteres_with_languages(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    offer = Offer(
        **{
            **MINIMAL_OFFER.__dict__,
            "languages": [Language(iso_code="EN", language_level=LanguageLevel.B2)],
        }
    )

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=offer))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["criteres"] == {
        "langues": [{"iso_code": "EN", "niveau": "B2"}]
    }


@pytest.mark.asyncio
async def test_publish_serializes_criteres_as_none_when_no_education_level(
    gateway, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=201)

    await gateway.publish(PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER))

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["offres"][0]["criteres"] is None


@pytest.mark.asyncio
async def test_publish_raises_on_http_error(gateway, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=PUBLISH_URL, status_code=500)

    with pytest.raises(httpx.HTTPStatusError):
        await gateway.publish(
            PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER)
        )


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
            "errors": [{"offer": {"reference": "2024-OFFER-001"}, "error": "invalid"}],
        },
    )

    with caplog.at_level("ERROR"), pytest.raises(ExternalApiError):
        await gateway.publish(
            PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER)
        )

    assert any("2024-OFFER-001" in record.getMessage() for record in caplog.records)


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
        await gateway.publish(
            PublishOfferInput(source_id=SOURCE_ID, offer=MINIMAL_OFFER)
        )

    assert caplog.records == []
