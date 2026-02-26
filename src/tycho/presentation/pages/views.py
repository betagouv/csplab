"""Home page view."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page view for CSPLab."""

    template_name = "pages/home.html"


class LegalNoticesView(TemplateView):
    """Legal notices page."""

    template_name = "pages/legal_notices.html"
