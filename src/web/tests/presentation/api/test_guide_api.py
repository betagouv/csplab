import pytest
import yaml
from django.conf import settings

_HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _public_routes() -> list[str]:
    schema = yaml.safe_load((settings.STATIC_DIR / "api" / "schema.yaml").read_text())
    return [
        f"{method.upper()} {path}"
        for path, operations in schema["paths"].items()
        for method in operations
        if method in _HTTP_METHODS
    ]


@pytest.mark.parametrize("route", _public_routes())
def test_guide_mentions_every_public_route(route):
    guide = (settings.STATIC_DIR / "api" / "guide_api.md").read_text()

    assert f"`{route}`" in guide
