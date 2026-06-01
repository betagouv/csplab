import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from api.main import create_app
from domain.raw_offer import RawOffer
from domain.source import Source
from domain.webhook_event import TalentsoftEventType
from tests.conftest import (
    SOURCE_ID,
    TALENTSOFT_BACK_BASE_URL,
    TALENTSOFT_BACK_CLIENT_ID,
    TALENTSOFT_BACK_CLIENT_SECRET,
    TALENTSOFT_FRONT_BASE_URL,
    TALENTSOFT_FRONT_CLIENT_ID,
    TALENTSOFT_FRONT_CLIENT_SECRET,
    make_signed_request,
    populate_sources_repository,
)
from tests.shared_fixtures import (
    TALENTSOFT_DETAIL_OFFER_URL,
    TALENTSOFT_TOKEN_URL,
    mock_talentsoft_token_response,
    setup_talentsoft_front_in_container,
)

REFERENCE = "2024-VACANCY-001"


def _coded_object():
    return {
        "code": 1,
        "clientCode": "CODE",
        "label": "Label",
        "active": True,
        "type": "type",
        "parentType": "",
    }


def _detail_offer_payload(reference: str = REFERENCE) -> dict:
    return {
        "reference": reference,
        "isTopOffer": False,
        "title": "Software Engineer",
        "organisationName": "ACME Corp",
        "organisationDescription": "A great company",
        "organisationLogoUrl": "https://example.com/logo.png",
        "modificationDate": "2024-01-01",
        "startPublicationDate": "2024-01-01",
        "offerUrl": "https://example.com/offer",
        "offerFamilyCategory": _coded_object(),
        "contractTypeCountry": _coded_object(),
    }


@pytest.mark.asyncio
async def test_vacancy_new_fetches_offer_details(
    talentsoft_client, httpx_mock: HTTPXMock
):
    mock_talentsoft_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=_detail_offer_payload(),
    )

    payload = {"event_type": TalentsoftEventType.VACANCY_NEW, "reference": REFERENCE}
    response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    requests = httpx_mock.get_requests()
    # token request + detail request
    assert len(requests) == 2
    token_req, detail_req = requests
    assert TALENTSOFT_TOKEN_URL in str(token_req.url)
    assert "reference=" + REFERENCE in str(detail_req.url)
    assert detail_req.headers["authorization"].startswith("Bearer ")


@pytest.mark.asyncio
async def test_vacancy_new_saves_raw_offer(talentsoft_client, httpx_mock: HTTPXMock):
    mock_talentsoft_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=_detail_offer_payload(),
    )

    payload = {"event_type": TalentsoftEventType.VACANCY_NEW, "reference": REFERENCE}
    make_signed_request(talentsoft_client, payload)

    mock_repo = talentsoft_client.app.state.mock_raw_offer_repository
    mock_repo.upsert.assert_called_once()
    saved: RawOffer = mock_repo.upsert.call_args[0][0]
    assert saved.reference == REFERENCE
    assert saved.source_id == SOURCE_ID
    assert saved.loaded_at is not None
    assert saved.error_msg is None
    assert saved.data is not None
    assert saved.data["reference"] == REFERENCE


@pytest.mark.asyncio
async def test_vacancy_update_fetches_offer_details(
    talentsoft_client, httpx_mock: HTTPXMock
):
    mock_talentsoft_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=_detail_offer_payload(),
    )

    payload = {"event_type": TalentsoftEventType.VACANCY_UPDATE, "reference": REFERENCE}
    response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert len(httpx_mock.get_requests()) == 2


@pytest.mark.asyncio
async def test_vacancy_new_talentsoft_not_configured_returns_500(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_BACK_BASE_URL", TALENTSOFT_BACK_BASE_URL)
    app = create_app()
    populate_sources_repository(app)
    client = TestClient(app, raise_server_exceptions=False)

    payload = {"event_type": TalentsoftEventType.VACANCY_NEW, "reference": REFERENCE}
    response = make_signed_request(client, payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Talentsoft client or database not configured"


@pytest.mark.asyncio
async def test_vacancy_new_talentsoft_api_error_propagates(
    monkeypatch, httpx_mock: HTTPXMock
):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_BACK_BASE_URL", TALENTSOFT_BACK_BASE_URL)
    app = create_app()
    setup_talentsoft_front_in_container(
        app,
        TALENTSOFT_FRONT_BASE_URL,
        TALENTSOFT_FRONT_CLIENT_ID,
        TALENTSOFT_FRONT_CLIENT_SECRET,
    )
    app.state.container.sources_repository().load(
        [
            Source(
                source_id=SOURCE_ID,
                type="talentsoft",
                client_id_front=TALENTSOFT_FRONT_CLIENT_ID,
                client_id_back=TALENTSOFT_BACK_CLIENT_ID,
                base_url_front=TALENTSOFT_FRONT_BASE_URL,
                base_url_back="https://talentsoft-back.example.com",
            )
        ]
    )
    client = TestClient(app, raise_server_exceptions=False)

    # The client has max_retries=2, so it will attempt 3 GET requests total.
    mock_talentsoft_token_response(httpx_mock)
    for _ in range(3):
        httpx_mock.add_response(
            method="GET",
            url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
            status_code=500,
        )

    payload = {"event_type": TalentsoftEventType.VACANCY_NEW, "reference": REFERENCE}
    response = make_signed_request(client, payload)

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_other_event_type_does_not_call_talentsoft(
    talentsoft_client, httpx_mock: HTTPXMock
):
    payload = {"event_type": "candidate_created", "reference": REFERENCE}
    response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert httpx_mock.get_requests() == []


@pytest.mark.asyncio
async def test_token_is_fetched_once_across_two_webhook_requests(
    talentsoft_client, httpx_mock: HTTPXMock
):
    reference_2 = "2024-VACANCY-002"

    mock_talentsoft_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=_detail_offer_payload(REFERENCE),
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={reference_2}",
        json=_detail_offer_payload(reference_2),
    )

    response_1 = make_signed_request(
        talentsoft_client, {"event_type": "vacancy_new", "reference": REFERENCE}
    )
    response_2 = make_signed_request(
        talentsoft_client, {"event_type": "vacancy_new", "reference": reference_2}
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    requests = httpx_mock.get_requests()
    # 1 token request + 2 detail requests.
    # token is not fetched again on the second webhook call
    assert len(requests) == 3
    token_requests = [r for r in requests if str(r.url) == TALENTSOFT_TOKEN_URL]
    assert len(token_requests) == 1
