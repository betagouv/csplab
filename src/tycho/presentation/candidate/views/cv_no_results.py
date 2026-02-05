"""CV no results view."""

from typing import Any
from uuid import UUID

from django.views.generic import TemplateView

from presentation.candidate.mixins import (
    BreadcrumbLink,
    BreadcrumbMixin,
)


class CVNoResultsView(BreadcrumbMixin, TemplateView):
    """View for CV no results page.

    Displays a message when no matching opportunities are found.
    """

    template_name: str = "candidate/cv_no_results.html"
    breadcrumb_current = "Aucun résultat trouvé"
    breadcrumb_links: list[BreadcrumbLink] = []

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add cv_uuid to context."""
        context = super().get_context_data(**kwargs)
        cv_uuid: UUID = kwargs["cv_uuid"]
        context["cv_uuid"] = cv_uuid
        return context
