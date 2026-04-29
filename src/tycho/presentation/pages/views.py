"""Home page view."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page view for CSPLab."""

    template_name = "pages/home.html"


class PrivacyView(TemplateView):
    """Privacy policy page."""

    template_name = "pages/privacy.html"
