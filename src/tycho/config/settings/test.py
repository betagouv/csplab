from config.settings.base import *  # noqa E402 F403

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

TALENTSOFT_BASE_URL = "https://fake-talentsoft.example.com"
TALENTSOFT_CLIENT_ID = "fake-client-id"
TALENTSOFT_CLIENT_SECRET = "fake-client-secret"  # noqa S105

TALENTSOFT_BACK_BASE_URL = "https://fake-talentsoft-back.example.com"
TALENTSOFT_BACK_CLIENT_ID = "fake-client-id"
TALENTSOFT_BACK_CLIENT_SECRET = "fake-client-secret"  # noqa S105

SENTRY_DNS = "example.com"

HUEY["immediate"] = False  # noqa: F405
