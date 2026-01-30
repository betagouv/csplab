"""CV upload flow views."""

import logging

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from presentation.candidate.forms.cv_flow import CVUploadForm
from presentation.candidate.mixins import (
    BreadcrumbLink,
    BreadcrumbMixin,
)

logger = logging.getLogger(__name__)


class CVUploadView(BreadcrumbMixin, FormView):
    """View for CV upload page.

    Displays the CV upload form and validates the uploaded PDF.
    """

    template_name = "candidate/cv_upload.html"
    form_class = CVUploadForm
    breadcrumb_current = "Recommandation de carrière"
    breadcrumb_links: list[BreadcrumbLink] = []
    success_url = reverse_lazy("candidate:cv_upload")  # TODO: change to next step URL

    def form_valid(self, form: CVUploadForm) -> HttpResponse:
        """Handle valid form submission."""
        cv_file = form.cleaned_data["cv_file"]
        logger.info(
            "CV upload validated: filename=%s, size=%d",
            cv_file.name,
            cv_file.size,
        )
        messages.success(self.request, "Votre CV a été validé avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form: CVUploadForm) -> HttpResponse:
        """Handle invalid form submission."""
        logger.warning("Form validation failed: %s", dict(form.errors))
        return super().form_invalid(form)


class CVProcessingView(BreadcrumbMixin, TemplateView):
    """View for CV confirmation/processing page."""

    template_name = "candidate/cv_processing.html"


class CVResultsView(BreadcrumbMixin, TemplateView):
    """View for CV analysis results page.

    Displays career opportunities matching the analyzed CV.
    """

    template_name = "candidate/cv_results.html"
    breadcrumb_current = "Résultat de l'analyse du CV"
    breadcrumb_links: list[BreadcrumbLink] = []

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add mock data for results display."""
        context = super().get_context_data(**kwargs)
        context["cv_name"] = "CV Adelle Mortelle.pdf"
        context["results"] = [
            {
                "type": "offer",
                "title": "Chef de projet transformation numérique",
                "description": "Pilotage de projets de modernisation des \
                  systèmes d'information.",
                "location": "Paris",
                "category": "Catégorie A",
                "versant": "État",
                "job_type": "Ingénieur des systèmes d'information",
                "url": "#",
            },
            {
                "type": "concours",
                "title": "Concours d'attaché d'administration de l'État",
                "description": "Recrutement d'attachés pour les ministères économiques \
                    et financiers.",
                "concours_type": "Externe",
                "category": "Catégorie A",
                "versant": "État",
                "job_type": "Attaché d'administration",
                "url": "#",
            },
            {
                "type": "offer",
                "title": "Responsable des ressources humaines",
                "description": "Gestion des carrières et accompagnement des agents.",
                "location": "Lyon",
                "category": "Catégorie A",
                "versant": "Territoriale",
                "job_type": "Attaché territorial",
                "url": "#",
            },
        ]
        context["results_count"] = len(context["results"])
        context["location_options"] = [
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
        return context
