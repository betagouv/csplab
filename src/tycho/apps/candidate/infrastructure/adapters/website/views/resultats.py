"""Results and opportunite detail views."""

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from apps.candidate.infrastructure.adapters.website.fixtures.mock_opportunites import (
    MOCK_OPPORTUNITE_DETAIL,
    MOCK_OPPORTUNITES,
)
from apps.candidate.infrastructure.adapters.website.views.mixins import (
    BreadcrumbMixin,
    RequiresCVMixin,
)


class ResultatsAnalyseView(RequiresCVMixin, BreadcrumbMixin, TemplateView):
    """View for CV analysis results page.

    The cv_id is passed in the URL and verified by RequiresCVMixin.

    TODO: Replace mock data with AnalyzeCVUsecase when implemented.
    """

    template_name = "candidate/resultats_analyse.html"
    breadcrumb_current = "Résultat de l'analyse"
    breadcrumb_links = []

    def get_opportunites_filtrees(self, request):
        """Filter opportunites based on request parameters."""
        opportunites = [opp.copy() for opp in MOCK_OPPORTUNITES]

        location = request.GET.get("location", "")
        if location:
            opportunites = [o for o in opportunites if o["location"] == location]

        category = request.GET.get("category", "")
        if category:
            opportunites = [o for o in opportunites if o["category"] == category]

        branches = request.GET.getlist("branch")
        if branches:
            opportunites = [o for o in opportunites if o["branch_key"] in branches]

        for opp in opportunites:
            opp["detail_url"] = reverse("candidate:opportunite_detail", kwargs={"pk": opp["id"]})

        return opportunites

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opportunites"] = self.get_opportunites_filtrees(self.request)
        context["cv_data"] = self.get_cv_data()

        context["active_filters"] = {
            "location": self.request.GET.get("location", ""),
            "category": self.request.GET.get("category", ""),
            "branches": self.request.GET.getlist("branch"),
        }
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET requests, with HTMX partial rendering."""
        context = self.get_context_data(**kwargs)

        if request.headers.get("HX-Request"):
            return render(
                request,
                "candidate/components/opportunite_list.html",
                context,
            )

        return render(request, self.template_name, context)


class OpportuniteDetailView(BreadcrumbMixin, TemplateView):
    """View for opportunite detail page.

    TODO: Add cv_id in URL to rebuild breadcrumb link.
    TODO: Replace mock data with real data when implemented.
    """

    template_name = "candidate/opportunite_detail.html"
    breadcrumb_current = ""
    breadcrumb_links = []

    def get_breadcrumb_data(self):
        """Return breadcrumb data with dynamic current title."""
        title = MOCK_OPPORTUNITE_DETAIL["title"]
        truncated_title = title[:30] + "..." if len(title) > 30 else title
        return {
            "links": self.breadcrumb_links,
            "current": truncated_title,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opportunite"] = MOCK_OPPORTUNITE_DETAIL
        return context
