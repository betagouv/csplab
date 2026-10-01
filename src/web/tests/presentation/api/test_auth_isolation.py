"""Every DRF view declares its authentication through exactly one mixin.

The mixins live in `presentation/api/authentication.py`: each one fixes both the
authenticators and the permissions of a view, so public (JWT / API key) and
internal (session) endpoints cannot silently share credentials.
"""

from django.urls import URLPattern, URLResolver, get_resolver
from rest_framework.views import APIView

from presentation.api.authentication import (
    PublicApiKeyOnlyMixin,
    PublicApiMixin,
    PublicJwtOnlyMixin,
    SessionApiMixin,
    UnauthenticatedMixin,
)

AUTH_MIXINS = (
    PublicApiMixin,
    PublicJwtOnlyMixin,
    PublicApiKeyOnlyMixin,
    SessionApiMixin,
    UnauthenticatedMixin,
)


def _drf_views(patterns=None, prefix=""):
    """Yield (path, view class) for every DRF view reachable from the URL conf."""
    for pattern in patterns if patterns is not None else get_resolver().url_patterns:
        path = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            yield from _drf_views(pattern.url_patterns, path)
        elif isinstance(pattern, URLPattern):
            view = getattr(pattern.callback, "cls", None)
            if view and issubclass(view, APIView):
                yield "/" + path, view


def test_every_drf_view_uses_exactly_one_authentication_mixin():
    views = list(_drf_views())
    assert views, "no DRF view found: the URL walk is broken"

    offenders = [
        f"{path} ({view.__name__}): {mixins} auth mixins"
        for path, view in views
        if (mixins := sum(issubclass(view, mixin) for mixin in AUTH_MIXINS)) != 1
    ]

    assert not offenders, "\n".join(offenders)
