"""CV upload flow views."""

import logging

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from presentation.candidate.forms.cv_flow import CVUploadForm
from presentation.candidate.mixins import BreadcrumbLink, BreadcrumbMixin

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
