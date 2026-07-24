import json
from functools import lru_cache
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@lru_cache(maxsize=1)
def _load_manifest_cached() -> dict:
    manifest_path = Path(settings.STATIC_DIR) / "frontend" / "manifest.json"
    if not manifest_path.exists():
        return {}

    with open(manifest_path) as f:
        return json.load(f)


def _load_manifest() -> dict:
    if settings.DEBUG:
        _load_manifest_cached.cache_clear()
    return _load_manifest_cached()


@register.simple_tag
def vite_dev_asset(path: str) -> str:
    return f"{settings.VITE_DEV_ORIGIN.rstrip('/')}/{path}"


@register.simple_tag
def vite_asset(entry: str) -> str:
    manifest = _load_manifest()

    if entry not in manifest:
        return static(f"frontend/{entry}")

    file_path = manifest[entry].get("file", entry)
    return static(f"frontend/{file_path}")


@register.simple_tag
def vite_css(entry: str) -> str:
    manifest = _load_manifest()

    if entry not in manifest:
        return ""

    css_files = manifest[entry].get("css", [])
    links = [
        f'<link rel="stylesheet" href="{static(f"frontend/{css}")}">'
        for css in css_files
    ]
    return mark_safe("\n".join(links))  # noqa: S308
