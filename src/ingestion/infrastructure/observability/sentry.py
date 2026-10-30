import logging
from collections.abc import Sequence

import sentry_sdk
from sentry_sdk.integrations import Integration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from api.config import Settings

SENSITIVE_KEYS = {
    "password",
    "token",
    "secret",
    "api_key",
    "authorization",
    "username",
    "email",
    "ip_address",
}


def scrub_dict(d: dict) -> dict:
    return {k: "[Filtered]" if k.lower() in SENSITIVE_KEYS else v for k, v in d.items()}


def strip_sentry_sensitive_data(event, hint):
    request = event.get("request", {})
    if "data" in request:
        if isinstance(request["data"], dict):
            request["data"] = scrub_dict(request["data"])

    if "headers" in request:
        request["headers"] = scrub_dict(request["headers"])

    return event


def init_sentry(
    settings: Settings,
    integrations: Sequence[Integration] = (),
    *,
    tracing: bool,
) -> None:
    """Single Sentry entry point for the API, the Celery worker and the scripts.

    Does nothing without SENTRY_DSN (local runs, tests).
    """
    if not settings.sentry_dsn or not str(settings.sentry_dsn).strip():
        return

    sentry_sdk.init(
        dsn=str(settings.sentry_dsn),
        integrations=[
            # Info logs as breadcrumbs, error logs as events.
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            HttpxIntegration(),
            *integrations,
        ],
        # DO NOT associate users (ID+email+username+IP) to errors
        send_default_pii=False,
        before_send=strip_sentry_sensitive_data,
        # Scripts only report errors: None disables tracing and profiling.
        traces_sample_rate=settings.sentry_traces_sample_rate if tracing else None,
        profiles_sample_rate=(
            settings.sentry_profiles_sample_rate if tracing else None
        ),
        before_send_transaction=strip_sentry_sensitive_data if tracing else None,
    )
