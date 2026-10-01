from http import HTTPStatus

from django.contrib.admin import AdminSite
from django.http import HttpRequest, HttpResponse
from django_otp.admin import OTPAdminSite

from application.identite.context_services.login_log import (
    log_admin_login_failed,
    log_admin_login_succeeded,
)


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
                log_admin_login_succeeded(request.user)
            else:
                log_admin_login_failed(request.POST.get("username", ""))
        return response


class LoggedAdminSite(LoginLoggingAdminSiteMixin, AdminSite):
    pass


class LoggedOTPAdminSite(LoginLoggingAdminSiteMixin, OTPAdminSite):
    pass
