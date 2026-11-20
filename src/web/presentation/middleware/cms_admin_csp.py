from django.conf import settings
from django.utils.csp import CSP


class CmsAdminCspMiddleware:
    """Relaxes the CSP and the framing rules on the Wagtail admin only.

    The admin runs inline scripts and styles without nonce, and previews pages in
    a same-origin iframe. Listed after ContentSecurityPolicyMiddleware and
    XFrameOptionsMiddleware, so that it sees the response first.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        prefix = f"/{settings.WAGTAILADMIN_PATH.lstrip('/')}"
        if request.path.startswith(prefix):
            policy = {**settings.SECURE_CSP}
            for directive in ("script-src", "script-src-elem"):
                policy[directive] = [CSP.SELF, CSP.UNSAFE_INLINE]
            for directive in ("style-src", "style-src-elem"):
                policy[directive] = [CSP.SELF, CSP.UNSAFE_INLINE]
            response._csp_config = policy
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response
