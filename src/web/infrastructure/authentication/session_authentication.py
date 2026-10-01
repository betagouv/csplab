from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import SessionAuthentication


class SessionApiAuthentication(SessionAuthentication):
    """Session authentication that answers 401 (not 403) when not authenticated.

    With `SessionAuthentication` alone, the first authenticator is the session
    one, which returns `None` there, so calls would turn into 403.
    Overriding `authenticate_header` keeps 401, which is also the more accurate
    status for "no valid credentials".

    Authentication itself (user read from the session cookie) and the CSRF
    enforcement on unsafe methods are inherited as-is from DRF.
    """

    def authenticate_header(self, request):
        return "Session"


class SessionApiAuthenticationScheme(OpenApiAuthenticationExtension):
    # drf-spectacular does not match subclasses of SessionAuthentication, so the
    # `cookieAuth` scheme has to be declared again for this class.
    target_class = SessionApiAuthentication
    name = "cookieAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": settings.SESSION_COOKIE_NAME,
        }
