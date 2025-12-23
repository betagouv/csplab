"""Reusable mixins for candidate views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

from apps.candidate.container_factory import create_candidate_container

if TYPE_CHECKING:
    from django.http import HttpRequest

    from core.entities.cv_metadata import CVMetadata


class RequiresCVMixin:
    """Mixin for views that require a valid CV in the URL.

    Verifies that the cv_id passed in the URL corresponds to an existing CV.
    Redirects to the upload page if the CV does not exist.

    Must be used with Django class-based views that have a dispatch method.
    """

    cv_required_message: str = "CV non trouvé. Veuillez uploader votre CV."
    cv_metadata: CVMetadata | None = None

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Verify CV exists before processing request."""
        cv_id = kwargs.get("cv_id")
        if not cv_id:
            messages.warning(request, self.cv_required_message)
            return redirect("candidate:cv_upload")

        try:
            container = create_candidate_container()
            cv_metadata_repository = container.cv_metadata_repository()
            self.cv_metadata = cv_metadata_repository.find_by_id(cv_id)

            if not self.cv_metadata:
                messages.warning(request, self.cv_required_message)
                return redirect("candidate:cv_upload")

        except Exception:
            messages.error(request, "Erreur lors de la récupération du CV.")
            return redirect("candidate:cv_upload")

        # Mypy can't infer the parent class in mixins, but we know it's a View
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]

    def get_cv_data(self) -> dict:
        """Return CV data for template context."""
        if self.cv_metadata:
            return {
                "name": self.cv_metadata.filename,
                "id": str(self.cv_metadata.id),
            }
        return {}


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
        # Mypy can't infer the parent class in mixins,
        # but we know it has get_context_data
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        context["breadcrumb_data"] = self.get_breadcrumb_data()
        return context
