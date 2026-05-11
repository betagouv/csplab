import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

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


sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs.
    event_level=logging.ERROR,  # Send errors as events.
)


def sentry_init(dsn, traces_sample_rate, profiles_sample_rate):
    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            sentry_logging,
            HttpxIntegration(),
            StarletteIntegration(),
            FastApiIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=traces_sample_rate,
        # To set a uniform sample rate
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production
        profiles_sample_rate=profiles_sample_rate,
        # DO NOT Associate users (ID+email+username+IP) to errors
        # set send_default_pii to False
        send_default_pii=False,
        # Filter out sensitive data in request
        before_send=strip_sentry_sensitive_data,
        before_send_transaction=strip_sentry_sensitive_data,
    )
