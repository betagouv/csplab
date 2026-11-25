from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class CmsAdminOTPMiddleware:
    """Requires an OTP-verified session to reach the Wagtail admin.

    Unverified visitors are sent to the Django admin login, which already asks
    for the one-time code, then come back to the page they asked for.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        prefix = f"/{settings.WAGTAILADMIN_PATH.lstrip('/')}"
        if settings.ADMIN_OTP_REQUIRED and request.path.startswith(prefix):
            user = request.user
            if not (user.is_authenticated and user.is_verified()):
                query = urlencode({"next": request.get_full_path()})
                return redirect(f"{reverse('admin:login')}?{query}")
        return self.get_response(request)
