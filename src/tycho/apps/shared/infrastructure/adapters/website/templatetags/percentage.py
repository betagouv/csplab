"""Template filters for percentage formatting."""

from django import template

register = template.Library()


@register.filter("pct")
def percentage(value):
    """Convert a decimal value to percentage format.

    Args:
        value: Float between 0 and 1

    Returns:
        String formatted as percentage (e.g., "85%")
    """
    try:
        return f"{float(value) * 100:.0f}%"
    except (ValueError, TypeError):
        return "0%"
