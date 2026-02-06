"""CV upload flow views."""

import asyncio
import threading
from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.di.candidate.candidate_factory import create_candidate_container
from presentation.candidate.forms.cv_flow import CVUploadForm
from presentation.candidate.mappers import (
    ConcoursToTemplateMapper,
    OfferToTemplateMapper,
)
from presentation.candidate.mixins import (
    BreadcrumbLink,
    BreadcrumbMixin,
)


class CVUploadView(BreadcrumbMixin, FormView):
    """View for CV upload page.

    Displays the CV upload form and validates the uploaded PDF.
    """

    template_name = "candidate/cv_upload.html"
    form_class = CVUploadForm
    breadcrumb_current = "Recommandation de carrière"
    breadcrumb_links: list[BreadcrumbLink] = []
    success_url = reverse_lazy("candidate:cv_upload")  # TODO: change to next step URL

    def __init__(self, *args, **kwargs):
        """Initialize view with dependency injection."""
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()
        self.logger = self.container.logger_service().get_logger(
            "CANDIDATE::INFRASTRUCTURE::CVUploadView"
        )

    def form_valid(self, form: CVUploadForm) -> HttpResponse:
        """Handle valid form submission."""
        cv_file = form.cleaned_data["cv_file"]
        self.logger.info(
            "CV upload validated: filename=%s, size=%d",
            cv_file.name,
            cv_file.size,
        )

        # Initialize CV metadata
        initialize_cv_metadata_usecase = self.container.initialize_cv_metadata_usecase()
        cv_uuid = initialize_cv_metadata_usecase.execute(cv_file.name)

        # Launch async CV processing
        process_uploaded_cv_usecase = self.container.process_uploaded_cv_usecase()
        thread = threading.Thread(
            target=lambda: asyncio.run(
                process_uploaded_cv_usecase.execute(UUID(cv_uuid), cv_file.read())
            )
        )
        thread.start()

        return redirect("candidate:cv_results", cv_uuid=cv_uuid)

    def form_invalid(self, form: CVUploadForm) -> HttpResponse:
        """Handle invalid form submission."""
        self.logger.warning("Form validation failed: %s", dict(form.errors))
        return super().form_invalid(form)


class CVResultsView(BreadcrumbMixin, TemplateView):
    """CV analysis results with HTMX polling support."""

    breadcrumb_current = "Résultat de l'analyse du CV"
    breadcrumb_links: list[BreadcrumbLink] = []

    def __init__(self, *args, **kwargs):
        """Initialize view with dependency injection."""
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()
        self.logger = self.container.logger_service().get_logger(
            "CANDIDATE::INFRASTRUCTURE::CVResultsView"
        )
        self.status = None
        self.opportunities = None
        self.filename = None

    def dispatch(self, request, *args, **kwargs):
        """Initialize status and opportunities once per request."""
        status_data = self._get_cv_processing_status()
        self.status = status_data.get("status")
        self.opportunities = status_data.get("opportunities", [])
        self.filename = status_data.get("filename")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET request with status-based routing."""
        is_htmx = request.headers.get("HX-Request")

        if self.status == CVStatus.PENDING and is_htmx:
            response = HttpResponse(status=204)
            response["HX-Reswap"] = "none"
            return response

        if self.status == CVStatus.FAILED:
            messages.error(
                request,
                "Une erreur est survenue lors du traitement de votre CV. "
                "Veuillez réessayer.",
            )
            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response["HX-Redirect"] = str(reverse_lazy("candidate:cv_upload"))
                return response
            return redirect("candidate:cv_upload")

        return super().get(request, *args, **kwargs)

    def _get_cv_processing_status(self) -> dict[str, object]:
        """Get CV processing status from repository."""
        cv_uuid = self.kwargs.get("cv_uuid")
        self.logger.info("Getting CV processing status for cv_uuid=%s", cv_uuid)

        cv_metadata_repository = self.container.postgres_cv_metadata_repository()
        opportunities = []
        filename = None
        try:
            cv_metadata = cv_metadata_repository.find_by_id(cv_uuid)

            status = cv_metadata.status if cv_metadata else CVStatus.PENDING
            filename = cv_metadata.filename

            if cv_metadata and status == CVStatus.COMPLETED:
                match_cv_to_opportunities = (
                    self.container.match_cv_to_opportunities_usecase()
                )
                raw_opportunities = match_cv_to_opportunities.execute(
                    cv_metadata=cv_metadata,
                    limit=10,
                )

                for opportunity in raw_opportunities:
                    if isinstance(opportunity[0], Concours):
                        opportunities.append(
                            ConcoursToTemplateMapper.map(opportunity[0])
                        )
                    elif isinstance(opportunity[0], Offer):
                        opportunities.append(OfferToTemplateMapper.map(opportunity[0]))

        except Exception:
            status = CVStatus.FAILED

        result: dict[str, object] = {
            "status": status,
            "opportunities": opportunities,
            "filename": filename,
        }

        return result

    def get_template_names(self) -> list[str]:
        """Route to appropriate template based on status and HTMX context."""
        is_htmx = self.request.headers.get("HX-Request")
        hx_target = self.request.headers.get("HX-Target")
        if self.status == CVStatus.PENDING:
            return (
                ["candidate/components/_processing_content.html"]
                if is_htmx
                else ["candidate/cv_processing.html"]
            )
        elif self.status == CVStatus.COMPLETED and not self.opportunities:
            return (
                ["candidate/components/_no_results_content.html"]
                if is_htmx
                else ["candidate/cv_results.html"]
            )
        elif is_htmx:
            return (
                ["candidate/components/_results_list.html"]
                if hx_target == "results-zone"
                else ["candidate/components/_results_content.html"]
            )

        # Default template for completed status with results
        return ["candidate/cv_results.html"]

    def _filter_results(self, results: list[dict[str, str]]) -> list[dict[str, str]]:
        """Filter results based on GET parameters."""
        location = self.request.GET.get("filter-location")
        category = self.request.GET.get("filter-category")

        filtered = results
        if location:
            filtered = [r for r in filtered if r.get("location_value") == location]
        if category:
            filtered = [r for r in filtered if r.get("category_value") == category]

        return filtered

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add mock data for results display."""
        context = super().get_context_data(**kwargs)

        context["cv_uuid"] = self.kwargs.get("cv_uuid")
        context["poll_interval"] = settings.CV_PROCESSING_POLL_INTERVAL

        if self.status == CVStatus.PENDING:
            return context

        context["cv_name"] = self.filename

        # TODO We may want to use a template tag to count opportunities to display,
        # and get context lighter.
        if isinstance(self.opportunities, list):
            context["results"] = self._filter_results(self.opportunities)
            context["results_count"] = len(context["results"])
        context["location_options"] = [
            {"value": "", "text": "Toutes les localisations"},
            {"value": "paris", "text": "Paris"},
            {"value": "lyon", "text": "Lyon"},
            {"value": "marseille", "text": "Marseille"},
            {"value": "bordeaux", "text": "Bordeaux"},
        ]
        context["location_default"] = {
            "disabled": True,
            "text": "Sélectionner une localisation",
        }
        context["category_options"] = [
            {"value": "", "text": "Toutes les catégories"},
            {"value": "a", "text": "Catégorie A"},
            {"value": "b", "text": "Catégorie B"},
            {"value": "c", "text": "Catégorie C"},
        ]
        context["category_default"] = {
            "disabled": True,
            "text": "Sélectionner une catégorie",
        }
        context["versants"] = [
            {"label": "Fonction publique d'État"},
            {"label": "Fonction publique Territoriale"},
            {"label": "Fonction publique Hospitalière"},
        ]
        context["results_target_id"] = "results-zone"
        return context
