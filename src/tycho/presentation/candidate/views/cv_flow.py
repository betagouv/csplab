"""CV upload flow views."""

from django.views.generic import TemplateView
import logging
from typing import Any

from presentation.candidate.mixins import BreadcrumbMixin

logger = logging.getLogger(__name__)


class CVUploadView(BreadcrumbMixin, TemplateView):
    """View for CV upload page."""

    template_name = "candidate/cv_upload.html"
    breadcrumb_current = "Recommandation de carrière"
    breadcrumb_links: list[dict[str, Any]] = []
