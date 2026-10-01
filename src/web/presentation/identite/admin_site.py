from http import HTTPStatus

from django.contrib.admin import AdminSite
from django.http import HttpRequest, HttpResponse
from django_otp.admin import OTPAdminSite

from application.identite.context_services.login_log import (
    log_login_failed,
    log_login_succeeded,
)
from infrastructure.django_apps.commons.enums import Canal
from infrastructure.django_apps.utils.ip import get_client_ip


class LoginLoggingAdminSiteMixin:
    def login(
        self, request: HttpRequest, extra_context: dict | None = None
    ) -> HttpResponse:
        response = super().login(request, extra_context)  # type: ignore[misc]
        # A POST with `otp_challenge` only asks for a code: it is not an attempt.
        if request.method == "POST" and "otp_challenge" not in request.POST:
            if (
                response.status_code == HTTPStatus.FOUND
                and request.user.is_authenticated
            ):
                log_login_succeeded(
                    canal=Canal.ADMIN,
                    user=request.user,
                    ip_address=get_client_ip(request),
                )
            else:
                log_login_failed(
                    canal=Canal.ADMIN,
                    email=request.POST.get("username", ""),
                    ip_address=get_client_ip(request),
                )
        return response


class LoggedAdminSite(LoginLoggingAdminSiteMixin, AdminSite):
    pass


class LoggedOTPAdminSite(LoginLoggingAdminSiteMixin, OTPAdminSite):
    pass
