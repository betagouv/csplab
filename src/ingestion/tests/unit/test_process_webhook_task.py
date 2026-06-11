from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import httpx
import pytest
from celery.app.task import Task
from celery.exceptions import Retry

from domain.value_objects.webhook_event import EventType, OfferStatus
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.tasks.process_webhook import _is_transient, process_webhook
from tests.factories.domain_factories import SourceFactory, WebhookFactory

WEBHOOK_ID = UUID("11111111-2222-3333-4444-555555555555")
REFERENCE = "2024-REF-001"
SOURCE_ID = "source-abc"
CLIENT_ID_FRONT = "front-client-id"
_PATCH_CONTAINER = "infrastructure.tasks.process_webhook.get_container"


def _make_mock_container(webhook=None) -> MagicMock:
    container = MagicMock()
    container.webhook_repository.return_value.get_by_id = AsyncMock(
        return_value=webhook
    )
    container.archive_offer_use_case.return_value.execute = AsyncMock()
    container.ingest_offer_pipeline.return_value.execute = AsyncMock()
    source = SourceFactory.build(source_id=SOURCE_ID, client_id_front=CLIENT_ID_FRONT)
    container.sources_repository.return_value.get_by_source_id.return_value = source
    return container


# --- Archive path ---


def test_archive_called_for_supprime_event():
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID,
        source_id=SOURCE_ID,
        event_type=EventType.SUPPRIME,
        reference=REFERENCE,
    )
    container = _make_mock_container(webhook)

    with patch(_PATCH_CONTAINER, return_value=container):
        process_webhook(str(WEBHOOK_ID))

    container.archive_offer_use_case.return_value.execute.assert_awaited_once_with(
        reference=REFERENCE, source_id=SOURCE_ID
    )


_NON_DIFFUSE_STATUSES = [s for s in OfferStatus if s != OfferStatus.DIFFUSE]


@pytest.mark.parametrize("status_id", _NON_DIFFUSE_STATUSES)
def test_archive_called_for_statut_change_non_diffuse(status_id: OfferStatus):
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID,
        source_id=SOURCE_ID,
        reference=REFERENCE,
        event_type=EventType.STATUT_CHANGE,
        status_id=str(status_id),
    )
    container = _make_mock_container(webhook)

    with patch(_PATCH_CONTAINER, return_value=container):
        process_webhook(str(WEBHOOK_ID))

    container.archive_offer_use_case.return_value.execute.assert_awaited_once_with(
        reference=REFERENCE, source_id=SOURCE_ID
    )


def test_no_action_for_statut_change_diffuse():
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID,
        source_id=SOURCE_ID,
        reference=REFERENCE,
        event_type=EventType.STATUT_CHANGE,
        status_id=str(OfferStatus.DIFFUSE),
    )
    container = _make_mock_container(webhook)

    with patch(_PATCH_CONTAINER, return_value=container):
        process_webhook(str(WEBHOOK_ID))

    container.archive_offer_use_case.return_value.execute.assert_not_called()
    container.sources_repository.return_value.get_by_source_id.assert_not_called()


# --- Ingest path ---


def test_ingest_pipeline_called_for_cree_event():
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID,
        source_id=SOURCE_ID,
        event_type=EventType.CREE,
        reference=REFERENCE,
    )
    container = _make_mock_container(webhook)

    with patch(_PATCH_CONTAINER, return_value=container):
        process_webhook(str(WEBHOOK_ID))

    container.ingest_offer_pipeline.return_value.execute.assert_awaited_once_with(
        reference=REFERENCE, source_id=SOURCE_ID
    )


def test_ingest_pipeline_called_for_mis_a_jour_event():
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID,
        source_id=SOURCE_ID,
        event_type=EventType.MIS_A_JOUR,
        reference=REFERENCE,
    )
    container = _make_mock_container(webhook)

    with patch(_PATCH_CONTAINER, return_value=container):
        process_webhook(str(WEBHOOK_ID))

    container.ingest_offer_pipeline.return_value.execute.assert_awaited_once_with(
        reference=REFERENCE, source_id=SOURCE_ID
    )


def test_ingest_raises_when_source_not_found():
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID, source_id=SOURCE_ID, event_type=EventType.CREE
    )
    container = _make_mock_container(webhook)
    container.sources_repository.return_value.get_by_source_id.return_value = None

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        pytest.raises(ValueError, match=SOURCE_ID),
    ):
        process_webhook(str(WEBHOOK_ID))


def test_ingest_raises_when_talentsoft_client_not_found():
    webhook = WebhookFactory.build(
        id=WEBHOOK_ID, source_id=SOURCE_ID, event_type=EventType.CREE
    )
    container = _make_mock_container(webhook)
    container.talentsoft_client_repository.return_value.get.return_value = None

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        pytest.raises(ValueError, match=SOURCE_ID),
    ):
        process_webhook(str(WEBHOOK_ID))


# --- Edge cases ---


def test_raises_when_webhook_not_found_in_db():
    container = _make_mock_container()
    container.webhook_repository.return_value.get_by_id = AsyncMock(
        side_effect=ValueError(f"Webhook {WEBHOOK_ID} not found in database")
    )

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        pytest.raises(ValueError, match=str(WEBHOOK_ID)),
    ):
        process_webhook(str(WEBHOOK_ID))


# --- Retries ---


@pytest.mark.parametrize(
    "exc",
    [
        httpx.ConnectError("connection refused"),
        httpx.TimeoutException("timed out"),
        ExternalApiError("server error", status_code=500),
        ExternalApiError("gateway error", status_code=503),
    ],
)
def test_is_transient_true(exc):
    assert _is_transient(exc) is True


@pytest.mark.parametrize(
    "exc",
    [
        ValueError("not found"),
        RuntimeError("misconfigured"),
        ExternalApiError("bad request", status_code=400),
        ExternalApiError("not found", status_code=404),
    ],
)
def test_is_transient_false(exc):
    assert _is_transient(exc) is False


def test_retries_on_transport_error():
    container = _make_mock_container()
    exc = httpx.ConnectError("connection refused")
    container.webhook_repository.return_value.get_by_id = AsyncMock(side_effect=exc)

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        patch.object(Task, "retry", side_effect=Retry()) as mock_retry,
        pytest.raises(Retry),
    ):
        process_webhook(str(WEBHOOK_ID))

    mock_retry.assert_called_once()
    assert mock_retry.call_args.kwargs["exc"] is exc
    assert mock_retry.call_args.kwargs["countdown"] == 1  # 2**0


def test_retries_on_external_api_5xx():
    container = _make_mock_container()
    exc = ExternalApiError("server error", status_code=500)
    container.webhook_repository.return_value.get_by_id = AsyncMock(side_effect=exc)

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        patch.object(Task, "retry", side_effect=Retry()) as mock_retry,
        pytest.raises(Retry),
    ):
        process_webhook(str(WEBHOOK_ID))

    mock_retry.assert_called_once()
    assert mock_retry.call_args.kwargs["exc"] is exc


def test_no_retry_on_external_api_4xx():
    container = _make_mock_container()
    exc = ExternalApiError("bad request", status_code=400)
    container.webhook_repository.return_value.get_by_id = AsyncMock(side_effect=exc)

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        patch.object(Task, "retry") as mock_retry,
        pytest.raises(ExternalApiError),
    ):
        process_webhook(str(WEBHOOK_ID))

    mock_retry.assert_not_called()


def test_no_retry_on_value_error():
    container = _make_mock_container()
    container.webhook_repository.return_value.get_by_id = AsyncMock(
        side_effect=ValueError(f"Webhook {WEBHOOK_ID} not found in database")
    )

    with (
        patch(_PATCH_CONTAINER, return_value=container),
        patch.object(Task, "retry") as mock_retry,
        pytest.raises(ValueError),
    ):
        process_webhook(str(WEBHOOK_ID))

    mock_retry.assert_not_called()
