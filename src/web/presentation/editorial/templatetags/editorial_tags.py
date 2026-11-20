from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
def image_src(value: str) -> str:
    """Absolute URL or site path as is, otherwise a path under static files."""
    if not value:
        return ""
    if value.startswith(("http://", "https://", "/")):
        return value
    try:
        return static(value)
    except ValueError:
        return ""
