from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from presentation.dtos.talentsoft_webhook import (
    TalentsoftEventType,
    TalentsoftOfferStatus,
)
from tests.conftest import (
    TALENTSOFT_BACK_BASE_URL,
    TALENTSOFT_BACK_CLIENT_ID,
    TALENTSOFT_BACK_CLIENT_SECRET,
    WEB_API_KEY,
    WEB_BASE_URL,
    make_signed_request,
    populate_sources_repository,
)

REFERENCE = "2019-1234"


@pytest.mark.asyncio
async def test_vacancy_deleted_enqueues_task(talentsoft_client):
    payload = {
        "event_type": TalentsoftEventType.VACANCY_DELETED,
        "reference": REFERENCE,
    }
    with patch("api.routes.process_webhook") as mock_task:
        response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_task.delay.assert_called_once()
    webhook_id = mock_task.delay.call_args[0][0]
    assert isinstance(webhook_id, str)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_id",
    [
        status
        for status in TalentsoftOfferStatus
        if status != TalentsoftOfferStatus.DIFFUSE
    ],
)
async def test_vacancy_status_non_diffuse_enqueues_task(
    talentsoft_client, status_id: TalentsoftOfferStatus
):
    payload = {
        "event_type": TalentsoftEventType.VACANCY_STATUS,
        "reference": REFERENCE,
        "statusId": status_id,
    }
    with patch("api.routes.process_webhook") as mock_task:
        response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_task.delay.assert_called_once()


@pytest.mark.asyncio
async def test_vacancy_status_diffuse_saves_but_does_not_enqueue(talentsoft_client):
    payload = {
        "event_type": TalentsoftEventType.VACANCY_STATUS,
        "reference": REFERENCE,
        "statusId": TalentsoftOfferStatus.DIFFUSE,
    }
    with patch("api.routes.process_webhook") as mock_task:
        response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    mock_task.delay.assert_not_called()
    webhook_repo = talentsoft_client.app.state.container.webhook_repository()
    webhook_repo.insert.assert_called_once()


@pytest.mark.asyncio
async def test_other_event_type_returns_500(httpx_mock, monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_BACK_BASE_URL", TALENTSOFT_BACK_BASE_URL)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()
    populate_sources_repository(app)
    client = TestClient(app, raise_server_exceptions=False)
    payload = {"event_type": "candidate_created", "reference": REFERENCE}
    response = make_signed_request(client, payload)
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_unknown_client_id_returns_403(monkeypatch, httpx_mock):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_ID", TALENTSOFT_BACK_CLIENT_ID)
    monkeypatch.setenv("TALENTSOFT_BACK_CLIENT_SECRET", TALENTSOFT_BACK_CLIENT_SECRET)
    monkeypatch.setenv("TALENTSOFT_BACK_BASE_URL", TALENTSOFT_BACK_BASE_URL)
    monkeypatch.setenv("WEB_BASE_URL", WEB_BASE_URL)
    monkeypatch.setenv("WEB_API_KEY", WEB_API_KEY)
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    payload = {"event_type": "vacancy_deleted", "reference": REFERENCE}
    response = make_signed_request(client, payload)
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid client_id"
