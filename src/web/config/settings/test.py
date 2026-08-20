import os

from config.settings.base import *  # noqa E402 F403

# Give each pytest-xdist worker its own Redis DB. Django's RedisCache.clear()
# runs FLUSHDB, which ignores KEY_PREFIX and wipes the whole db, so a key
# prefix alone isn't enough to keep parallel workers from clobbering each
# other's throttle counters; a dedicated db per worker is.
_xdist_worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
_worker_index = (
    int(_xdist_worker.removeprefix("gw")) if _xdist_worker.startswith("gw") else 0
)
CACHES["default"]["LOCATION"] = (  # noqa: F405
    f"{env.str('REDIS_URL')}/?db={int(REDIS_CACHE_DB) + 1 + _worker_index}"  # noqa: F405
)

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

HUEY["immediate"] = True  # noqa: F405, run synchronously

# Override third-party API endpoints
PISTE_OAUTH_BASE_URL = "https://fake-piste-oauth.example.com"

INGRES_BASE_URL = "https://fake-ingres-api.example.com/path"
INGRES_CLIENT_ID = "fake-client-id"
INGRES_CLIENT_SECRET = "fake-client-secret"  # noqa S105

ALBERT_API_BASE_URL = "https://fake-albert.example.com"
ALBERT_API_KEY = "test-api-key"

PROCONNECT_CLIENT_ID = "fake-client-id"
PROCONNECT_CLIENT_SECRET = "fake-client-secret"  # noqa S105
PROCONNECT_BASE_URL = "https://fake-proconnect.example.com"

INGESTION_API_KEY = "test-ingestion-api-key"

SENTRY_DNS = "example.com"

HUEY["immediate"] = False  # noqa: F405
