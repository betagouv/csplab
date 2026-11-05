import logging
from uuid import UUID

from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.throttling import SimpleRateThrottle

from config.logger_names import LoggerName
from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.django_apps.utils.ip import get_client_ip

logger = logging.getLogger(LoggerName.IDENTITE)


class AuthRejectionRateThrottle(SimpleRateThrottle):
    """
    DRF authenticates before DEFAULT_THROTTLE_CLASSES: without this, every
    rejection would write an audit row with no limit.
    """

    scope = "auth_rejection"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": get_client_ip(request),
        }


def reject(
    request,
    *,
    canal: Canal,
    subject: str,
    reason: str,
    message: str,
    utilisateur_id: UUID | None = None,
) -> AuthenticationFailed | Throttled:
    throttle = AuthRejectionRateThrottle()
    if not throttle.allow_request(request, view=None):
        return Throttled(wait=throttle.wait())
    ip_address = get_client_ip(request)
    logger.warning("%s rejected (%s) from %s.", subject, reason, ip_address)
    AuditLoginLogModel.objects.record_attempt(
        canal=canal,
        resultat=Resultat.ECHEC,
        utilisateur_id=utilisateur_id,
        ip_address=ip_address,
    )
    return AuthenticationFailed(message)
