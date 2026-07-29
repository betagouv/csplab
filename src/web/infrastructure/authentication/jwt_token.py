from typing import Optional

from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework_simplejwt.tokens import Token


def get_validated_jwt(
    request: HttpRequest, authenticator: JWTAuthentication
) -> Optional[Token]:
    try:
        header = authenticator.get_header(request)
        if header is None:
            return None
        raw_token = authenticator.get_raw_token(header)
        if raw_token is None:
            return None
        return authenticator.get_validated_token(raw_token)
    except (AuthenticationFailed, TokenError):
        return None
