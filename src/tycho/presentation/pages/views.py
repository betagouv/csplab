"""Static page views."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page view for CSPLab."""

    template_name = "pages/home.html"


class AccessibilityView(TemplateView):
    """Accessibility statement page."""

    template_name = "pages/accessibility.html"
