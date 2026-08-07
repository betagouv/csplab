from authlib.integrations.base_client.errors import OAuthError
from authlib.integrations.django_client import OAuth
from django.conf import settings
from joserfc import jwt
from joserfc.jwk import KeySet

AUTHORIZATION_ENDPOINT = "/api/v2/authorize"
TOKEN_ENDPOINT = "/api/v2/token"  # noqa S105
USERINFO_ENDPOINT = "/api/v2/userinfo"
JWKS_ENDPOINT = "/api/v2/jwks"
END_SESSION_ENDPOINT = "/api/v2/session/end"

oauth = OAuth()
oauth.register(
    name="proconnect",
    client_id=settings.PROCONNECT_CLIENT_ID,
    client_secret=settings.PROCONNECT_CLIENT_SECRET,
    authorize_url=f"{settings.PROCONNECT_BASE_URL}{AUTHORIZATION_ENDPOINT}",
    access_token_url=f"{settings.PROCONNECT_BASE_URL}{TOKEN_ENDPOINT}",
    userinfo_endpoint=f"{settings.PROCONNECT_BASE_URL}{USERINFO_ENDPOINT}",
    jwks_uri=f"{settings.PROCONNECT_BASE_URL}{JWKS_ENDPOINT}",
    client_kwargs={
        "scope": "openid email given_name usual_name roles organization_label"
    },
)


def fetch_userinfo_claims(token: dict) -> dict:
    """Fetch and return the userinfo claims.

    ProConnect returns the userinfo response as a signed JWT rather than
    plain JSON, so a plain `.json()` read fails; fall back to verifying and
    decoding it with the same JWKS used for the ID token.
    """
    try:
        resp = oauth.proconnect.get(
            f"{settings.PROCONNECT_BASE_URL}{USERINFO_ENDPOINT}", token=token
        )
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            key_set = KeySet.import_key_set(oauth.proconnect.fetch_jwk_set())
            return dict(jwt.decode(resp.text, key=key_set).claims)
    except OAuthError:
        raise
    except Exception as exc:
        raise OAuthError(description=f"Invalid userinfo response: {exc}") from exc
