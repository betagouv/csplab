import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from api.main import create_app
from presentation.dtos.talentsoft_webhook import TalentsoftEventType
from tests.conftest import (
    TALENTSOFT_BACK_CLIENT_ID,
    TALENTSOFT_BACK_CLIENT_SECRET,
    TALENTSOFT_FRONT_BASE_URL,
    TALENTSOFT_FRONT_CLIENT_ID,
    TALENTSOFT_FRONT_CLIENT_SECRET,
    WEB_API_KEY,
    WEB_BASE_URL,
    make_signed_request,
)

REFERENCE = "2024-VACANCY-001"
TOKEN_URL = f"{TALENTSOFT_FRONT_BASE_URL}/api/token"
DETAIL_OFFER_URL = f"{TALENTSOFT_FRONT_BASE_URL}/api/v2/offers/getoffer"


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


def _mock_token_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="POST",
        url=TOKEN_URL,
        json={
            "access_token": "test-access-token",
            "token_type": "Bearer",
            "expires_in": 3600,
        },
    )


@pytest.mark.asyncio
async def test_vacancy_new_fetches_offer_details(
    talentsoft_client, httpx_mock: HTTPXMock
):
    _mock_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{DETAIL_OFFER_URL}?reference={REFERENCE}",
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
    assert TOKEN_URL in str(token_req.url)
    assert "reference=" + REFERENCE in str(detail_req.url)
    assert "Bearer test-access-token" in detail_req.headers["authorization"]


@pytest.mark.asyncio
async def test_vacancy_update_fetches_offer_details(
    talentsoft_client, httpx_mock: HTTPXMock
):
    _mock_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{DETAIL_OFFER_URL}?reference={REFERENCE}",
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
    monkeypatch.setenv("TALENTSOFT_FRONT_CLIENT_ID", TALENTSOFT_FRONT_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_FRONT_CLIENT_SECRET", TALENTSOFT_FRONT_CLIENT_SECRET)
    monkeypatch.delenv("TALENTSOFT_FRONT_BASE_URL", raising=False)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    payload = {"event_type": TalentsoftEventType.VACANCY_NEW, "reference": REFERENCE}
    response = make_signed_request(client, payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Talentsoft client not configured"


@pytest.mark.asyncio
async def test_vacancy_new_talentsoft_api_error_propagates(
    monkeypatch, httpx_mock: HTTPXMock
):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_FRONT_CLIENT_ID", TALENTSOFT_FRONT_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_FRONT_CLIENT_SECRET", TALENTSOFT_FRONT_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_FRONT_BASE_URL", TALENTSOFT_FRONT_BASE_URL)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    # The client has max_retries=2, so it will attempt 3 GET requests total.
    _mock_token_response(httpx_mock)
    for _ in range(3):
        httpx_mock.add_response(
            method="GET",
            url=f"{DETAIL_OFFER_URL}?reference={REFERENCE}",
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

    _mock_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=_detail_offer_payload(REFERENCE),
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{DETAIL_OFFER_URL}?reference={reference_2}",
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
    token_requests = [r for r in requests if str(r.url) == TOKEN_URL]
    assert len(token_requests) == 1
