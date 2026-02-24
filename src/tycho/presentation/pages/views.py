"""Home page view."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page view for CSPLab."""

    template_name = "pages/home.html"


class TermsView(TemplateView):
    """Terms and conditions page."""

    template_name = "pages/terms.html"
