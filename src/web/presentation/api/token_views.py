from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from application.identite.context_services.api_login_log import (
    log_api_login_failed,
    log_api_login_succeeded,
)


class LoggedTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        email = str(request.data.get("email", ""))
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            log_api_login_failed(email)
            raise
        log_api_login_succeeded(email)
        return response
