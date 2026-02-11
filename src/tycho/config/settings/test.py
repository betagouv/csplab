"""Django settings for tycho project in test mode."""

from config.settings.base import *  # noqa E402 F403

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Override settings for testing
PISTE_OAUTH_BASE_URL = "https://fake-piste-oauth.example.com"

INGRES_BASE_URL = "https://fake-ingres-api.example.com/path"
INGRES_CLIENT_ID = "fake-client-id"
INGRES_CLIENT_SECRET = "fake-client-secret"  # noqa S105

OPENROUTER_BASE_URL = "https://api.openai.com/v1"
OPENROUTER_API_KEY = "test-api-key"
OPENROUTER_EMBEDDING_MODEL = "text-embedding-3-large"
OPENROUTER_OCR_MODEL = "gpt-4o-mini"

ALBERT_API_BASE_URL = "https://albert.api.etalab.gouv.fr"
ALBERT_API_KEY = "test-albert-key"
ALBERT_OCR_MODEL = "albert-large"

TALENTSOFT_BASE_URL = "https://fake-talentsoft.example.com"
TALENTSOFT_CLIENT_ID = "fake-client-id"
TALENTSOFT_CLIENT_SECRET = "fake-client-secret"  # noqa S105
