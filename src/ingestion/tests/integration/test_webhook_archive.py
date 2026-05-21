import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from api.main import create_app
from tests.integration.conftest import (
    TALENTSOFT_CLIENT_ID,
    TALENTSOFT_CLIENT_SECRET,
    WEB_API_KEY,
    WEB_BASE_URL,
    make_signed_request,
)

REFERENCE = "2019-1234"
ARCHIVE_URL = f"{WEB_BASE_URL}/api/data/offres/archiver"


@pytest.mark.asyncio
async def test_vacancy_status_archived_calls_archive(
    talentsoft_client, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(method="POST", url=ARCHIVE_URL, status_code=200)
    payload = {
        "event_type": "vacancy_status",
        "reference": REFERENCE,
        "statusId": "_TS_Archived",
    }
    response = make_signed_request(talentsoft_client, payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == f"Api-Key {WEB_API_KEY}"


@pytest.mark.asyncio
async def test_vacancy_deleted_calls_archive(talentsoft_client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url=ARCHIVE_URL, status_code=200)
    payload = {"event_type": "vacancy_deleted", "reference": REFERENCE}
    response = make_signed_request(talentsoft_client, payload)
    assert response.status_code == 200
    assert len(httpx_mock.get_requests()) == 1


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
async def test_web_service_not_configured_returns_500(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_CLIENT_ID", TALENTSOFT_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_CLIENT_SECRET", TALENTSOFT_CLIENT_SECRET)
    monkeypatch.delenv("WEB_BASE_URL", raising=False)
    monkeypatch.delenv("WEB_API_KEY", raising=False)
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    payload = {"event_type": "vacancy_deleted", "reference": REFERENCE}
    response = make_signed_request(client, payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Web service not configured"
