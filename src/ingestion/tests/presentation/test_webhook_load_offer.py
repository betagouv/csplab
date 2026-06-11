from unittest.mock import patch

import pytest

from presentation.dtos.talentsoft_webhook import TalentsoftEventType
from tests.conftest import (
    make_signed_request,
)

REFERENCE = "2024-VACANCY-001"


@pytest.mark.asyncio
async def test_vacancy_new_enqueues_task(talentsoft_client):
    payload = {"event_type": TalentsoftEventType.VACANCY_NEW, "reference": REFERENCE}
    with patch("api.routes.process_webhook") as mock_task:
        response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_task.delay.assert_called_once()
    webhook_id = mock_task.delay.call_args[0][0]
    assert isinstance(webhook_id, str)


@pytest.mark.asyncio
async def test_vacancy_update_enqueues_task(talentsoft_client):
    payload = {"event_type": TalentsoftEventType.VACANCY_UPDATE, "reference": REFERENCE}
    with patch("api.routes.process_webhook") as mock_task:
        response = make_signed_request(talentsoft_client, payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_task.delay.assert_called_once()
