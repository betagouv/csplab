"""CV upload flow views."""

import asyncio
import threading
from uuid import UUID

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.di.candidate.candidate_factory import create_candidate_container
from presentation.candidate.forms.cv_flow import CVUploadForm
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

        messages.success(self.request, "Votre CV est en cours de traitement !")
        return redirect("candidate:cv_results", cv_uuid=cv_uuid)

    def form_invalid(self, form: CVUploadForm) -> HttpResponse:
        """Handle invalid form submission."""
        self.logger.warning("Form validation failed: %s", dict(form.errors))
        return super().form_invalid(form)


class CVResultsView(BreadcrumbMixin, TemplateView):
    """CV analysis results with HTMX polling support."""

    template_name: str = "candidate/cv_results.html"
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

    def dispatch(self, request, *args, **kwargs):
        """Initialize status and opportunities once per request."""
        status_data = self._get_cv_processing_status()
        self.status = status_data.get("status")
        self.opportunities = status_data.get("opportunities", [])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET request with FAILED status check."""
        status_data = self._get_cv_processing_status()
        status = status_data.get("status")

        if status == CVStatus.FAILED:
            messages.error(
                request,
                "Une erreur est survenue lors du traitement de votre CV. "
                "Veuillez réessayer.",
            )
            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response["HX-Redirect"] = reverse_lazy("candidate:cv_upload")
                return response
            return redirect("candidate:cv_upload")

        return super().get(request, *args, **kwargs)

    def _get_cv_processing_status(self) -> dict[str, object]:
        """Get CV processing status from repository.

        TODO: Replace with MatchCVToOpportunitiesUsecase(wait_for_completion=True)
        """
        cv_uuid = self.kwargs.get("cv_uuid")
        cv_metadata_repository = self.container.postgres_cv_metadata_repository()

        try:
            cv_metadata = cv_metadata_repository.find_by_id(cv_uuid)
            status = cv_metadata.status if cv_metadata else CVStatus.PENDING
        except Exception:
            status = CVStatus.PENDING

        result: dict[str, object] = {"status": status, "opportunities": []}

        # For demo: show mock results for any completed/failed status
        if status != CVStatus.PENDING:
            result["opportunities"] = self._get_mock_results()

        return result

    def get_template_names(self) -> list[str]:
        """Route to appropriate template based on status and HTMX context."""
        is_htmx = self.request.headers.get("HX-Request")

        if self.status == CVStatus.PENDING:
            if is_htmx:
                return ["candidate/components/_processing_content.html"]
            return ["candidate/cv_processing.html"]

        if is_htmx:
            hx_target = self.request.headers.get("HX-Target")
            if hx_target == "results-zone":
                return ["candidate/components/_results_list.html"]
            return ["candidate/components/_results_content.html"]

        return [self.template_name]

    def _get_mock_results(self) -> list[dict[str, str]]:
        """Return mock results data."""
        return [
            {
                "type": "offer",
                "title": "Chef de projet transformation numérique",
                "description": "Pilotage de projets de modernisation des "
                "systèmes d'information.",
                "location": "Paris",
                "location_value": "paris",
                "category": "Catégorie A",
                "category_value": "a",
                "versant": "État",
                "job_type": "Ingénieur des systèmes d'information",
                "url": "#",
            },
            {
                "type": "concours",
                "title": "Concours d'attaché d'administration de l'État",
                "description": "Recrutement d'attachés pour les ministères "
                "économiques et financiers.",
                "concours_type": "Externe",
                "category": "Catégorie A",
                "category_value": "a",
                "versant": "État",
                "job_type": "Attaché d'administration",
                "url": "#",
            },
            {
                "type": "offer",
                "title": "Responsable des ressources humaines",
                "description": "Gestion des carrières et accompagnement des agents.",
                "location": "Lyon",
                "location_value": "lyon",
                "category": "Catégorie A",
                "category_value": "a",
                "versant": "Territoriale",
                "job_type": "Attaché territorial",
                "url": "#",
            },
            {
                "type": "offer",
                "title": "Technicien informatique",
                "description": "Support et maintenance des systèmes.",
                "location": "Paris",
                "location_value": "paris",
                "category": "Catégorie B",
                "category_value": "b",
                "versant": "État",
                "job_type": "Technicien",
                "url": "#",
            },
        ]

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

        if self.status == CVStatus.PENDING:
            return context

        context["cv_name"] = "CV Adelle Mortelle.pdf"

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
