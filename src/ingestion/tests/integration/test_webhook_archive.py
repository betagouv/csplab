import json

import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from api.main import create_app
from tests.integration.conftest import (
    SOURCE_ID,
    TALENTSOFT_BACK_CLIENT_ID,
    TALENTSOFT_BACK_CLIENT_SECRET,
    WEB_API_KEY,
    WEB_BASE_URL,
    make_signed_request,
)

REFERENCE = "2019-1234"
ARCHIVE_URL = f"{WEB_BASE_URL}/api/v1/offres/archiver"


@pytest.mark.asyncio
async def test_vacancy_status_archived_calls_archive(
    talentsoft_client, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=ARCHIVE_URL, status_code=200)
    payload = {
        "event_type": "vacancy_status",
        "reference": REFERENCE,
        "statusId": "_TS_CO_OfferStatus_Archive",
    }
    response = make_signed_request(talentsoft_client, payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == f"Api-Key {WEB_API_KEY}"
    body = json.loads(requests[0].content)
    assert body["source_id"] == SOURCE_ID


@pytest.mark.asyncio
async def test_vacancy_deleted_calls_archive(talentsoft_client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=ARCHIVE_URL, status_code=200)
    payload = {"event_type": "vacancy_deleted", "reference": REFERENCE}
    response = make_signed_request(talentsoft_client, payload)
    assert response.status_code == 200
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    body = json.loads(requests[0].content)
    assert body["source_id"] == SOURCE_ID


@pytest.mark.asyncio
async def test_vacancy_status_other_does_not_call_archive(
    talentsoft_client, httpx_mock: HTTPXMock
):
    payload = {
        "event_type": "vacancy_status",
        "reference": REFERENCE,
        "statusId": "_TS_Validated",
    }
    response = make_signed_request(talentsoft_client, payload)
    assert response.status_code == 200
    assert httpx_mock.get_requests() == []


@pytest.mark.asyncio
async def test_other_event_type_does_not_call_archive(
    talentsoft_client, httpx_mock: HTTPXMock
):
    payload = {"event_type": "candidate_created", "reference": REFERENCE}
    response = make_signed_request(talentsoft_client, payload)
    assert response.status_code == 200
    assert httpx_mock.get_requests() == []


@pytest.mark.asyncio
async def test_unknown_client_id_returns_422(monkeypatch, httpx_mock: HTTPXMock):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()
    # Registry is empty — no source registered for this client_id
    client = TestClient(app, raise_server_exceptions=False)

    payload = {"event_type": "vacancy_deleted", "reference": REFERENCE}
    response = make_signed_request(client, payload)
    assert response.status_code == 422
    assert "client_id" in response.json()["detail"]


@pytest.mark.asyncio
async def test_web_service_not_configured_returns_500(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.delenv("WEB_BASE_URL", raising=False)
    monkeypatch.delenv("WEB_API_KEY", raising=False)
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    payload = {"event_type": "vacancy_deleted", "reference": REFERENCE}
    response = make_signed_request(client, payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Web service not configured"
