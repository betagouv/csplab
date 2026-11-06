from unittest.mock import AsyncMock, patch

from sentry_sdk.integrations.celery import CeleryIntegration

from api.config import Settings
from infrastructure.di import bootstrap
from infrastructure.observability.sentry import strip_sentry_sensitive_data

DSN = "https://key@o123.ingest.sentry.io/123"


@patch("infrastructure.di.bootstrap.init_container")
@patch("infrastructure.observability.sentry.sentry_sdk.init")
def test_worker_process_init_uses_shared_sentry_init(
    mock_sentry_init, mock_init_container
):
    settings = Settings(
        sentry_dsn=DSN,
        sentry_traces_sample_rate=0.2,
        sentry_profiles_sample_rate=0.3,
    )

    with patch.object(bootstrap, "settings", settings):
        bootstrap._init_worker_container()

    kwargs = mock_sentry_init.call_args.kwargs
    assert kwargs["send_default_pii"] is False
    assert kwargs["before_send"] is strip_sentry_sensitive_data
    assert kwargs["traces_sample_rate"] == 0.2
    assert any(isinstance(i, CeleryIntegration) for i in kwargs["integrations"])
    mock_init_container.assert_called_once()


@patch("infrastructure.di.container.create_container")
def test_init_container_loads_sources_and_metiers_multi_domaines(
    mock_create_container,
):
    container = mock_create_container.return_value
    container.load_sources_usecase.return_value.execute = AsyncMock()
    container.load_metiers_multi_domaines_usecase.return_value.execute = AsyncMock()

    bootstrap.init_container()

    container.load_sources_usecase.return_value.execute.assert_awaited_once()
    container.load_metiers_multi_domaines_usecase.return_value.execute.assert_awaited_once()
    assert bootstrap._state["container"] is container
    bootstrap._state["container"] = None
