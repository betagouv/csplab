"""CV upload flow views."""

import logging
from typing import Any

from django.views.generic import FormView

from presentation.candidate.forms.cv_flow import CVUploadForm
from presentation.candidate.mixins import BreadcrumbMixin

logger = logging.getLogger(__name__)


class CVUploadView(BreadcrumbMixin, FormView):
    """View for CV upload page.

    Displays the CV upload form and validates the uploaded PDF.
    """

    template_name = "candidate/cv_upload.html"
    form_class = CVUploadForm
    breadcrumb_current = "Recommandation de carrière"
    breadcrumb_links: list[dict[str, Any]] = []
