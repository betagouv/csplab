"""Reusable mixins for candidate views."""

from __future__ import annotations

from typing import Any


class BreadcrumbMixin:
    """Mixin to add breadcrumb data to context.

    Must be used with Django class-based views that have get_context_data.
    """

    breadcrumb_links: list[dict] = []
    breadcrumb_current: str = ""

    def get_breadcrumb_data(self) -> dict:
        """Return breadcrumb data for dsfr_breadcrumb tag."""
        return {
            "links": self.breadcrumb_links,
            "current": self.breadcrumb_current,
        }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add breadcrumb data to context."""
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        context["breadcrumb_data"] = self.get_breadcrumb_data()
        return context
