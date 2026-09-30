import time
from typing import Any

from django.conf import settings
from django.contrib.auth import load_backend
from django.http import HttpRequest
from django_otp import devices_for_user

PENDING_SESSION_KEY = "otp_pending"
PENDING_TTL_SECONDS = 300

NO_DEVICE_MESSAGE = (
    "Aucun appareil d'authentification à deux facteurs n'est configuré pour "
    "ce compte. Contactez un administrateur."
)


def requires_otp(user) -> bool:
    return settings.OTP_REQUIRED and (user.is_staff or user.is_superuser)


def has_confirmed_device(user) -> bool:
    return any(True for _ in devices_for_user(user, confirmed=True))


def start_challenge(
    request: HttpRequest,
    user,
    backend: str,
    *,
    next_url: str = "",
    oidc_id_token: str | None = None,
    audit: bool = False,
) -> None:
    """Park a first-factor success in the session until the TOTP is validated.

    The user is deliberately not logged in yet: there is no "authenticated but
    unverified" session to bypass by navigating away.
    """
    request.session[PENDING_SESSION_KEY] = {
        "user_id": user.pk,
        "backend": backend,
        "next_url": next_url,
        "oidc_id_token": oidc_id_token,
        "audit": audit,
        "started_at": time.time(),
    }


def get_pending(request: HttpRequest) -> dict[str, Any] | None:
    pending = request.session.get(PENDING_SESSION_KEY)
    if pending is None:
        return None
    if time.time() - pending["started_at"] > PENDING_TTL_SECONDS:
        clear_pending(request)
        return None
    return pending


def clear_pending(request: HttpRequest) -> None:
    request.session.pop(PENDING_SESSION_KEY, None)


def load_pending_user(pending: dict[str, Any]):
    return load_backend(pending["backend"]).get_user(pending["user_id"])
