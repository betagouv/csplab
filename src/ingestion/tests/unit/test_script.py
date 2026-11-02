from unittest.mock import AsyncMock, patch

from infrastructure.observability.script import run_script


@patch("infrastructure.observability.sentry.sentry_sdk.init")
def test_run_script_initializes_sentry_then_runs_coroutine(
    mock_sentry_init, monkeypatch
):
    monkeypatch.setenv("SENTRY_DSN", "https://key@o123.ingest.sentry.io/123")
    job = AsyncMock()

    run_script(job())

    mock_sentry_init.assert_called_once()
    assert mock_sentry_init.call_args.kwargs["traces_sample_rate"] is None
    job.assert_awaited_once()


@patch("infrastructure.observability.sentry.sentry_sdk.init")
def test_run_script_runs_without_sentry_when_no_dsn(mock_sentry_init, monkeypatch):
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    job = AsyncMock()

    run_script(job())

    mock_sentry_init.assert_not_called()
    job.assert_awaited_once()
