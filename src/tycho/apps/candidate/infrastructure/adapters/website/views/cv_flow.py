"""CV upload and confirmation flow views."""

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from apps.candidate.container_factory import create_candidate_container
from apps.candidate.infrastructure.adapters.website.forms import CVUploadForm
from apps.candidate.infrastructure.adapters.website.views.mixins import (
    BreadcrumbMixin,
    RequiresCVMixin,
)


class CVUploadView(BreadcrumbMixin, FormView):
    """View for CV upload page with Django form handling.

    Uses ProcessUploadedCVUsecase to process the uploaded CV.
    Redirects to confirmation page with cv_id in URL.
    """

    template_name = "candidate/cv_upload.html"
    form_class = CVUploadForm
    breadcrumb_current = "Recommandation de carrière"
    breadcrumb_links = []

    def form_valid(self, form):
        """Handle valid form submission by processing CV via usecase."""
        cv_file = form.cleaned_data["cv_file"]

        try:
            pdf_content = cv_file.read()

            container = create_candidate_container()
            process_cv_usecase = container.process_uploaded_cv_usecase()

            cv_id = process_cv_usecase.execute(
                filename=cv_file.name,
                pdf_content=pdf_content,
            )

            return redirect("candidate:cv_confirmation", cv_id=cv_id)

        except Exception as e:
            messages.error(
                self.request,
                f"Erreur lors du traitement du CV : {e!s}",
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submission."""
        for _field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class CVConfirmationView(RequiresCVMixin, BreadcrumbMixin, TemplateView):
    """View for CV confirmation/processing page.

    Displays a processing animation and redirects to results.
    The cv_id is passed in the URL and verified by RequiresCVMixin.
    """

    template_name = "candidate/cv_processing.html"
    breadcrumb_current = "Analyse en cours"
    redirect_delay_seconds = 5

    @property
    def breadcrumb_links(self):
        return [
            {"url": reverse("candidate:cv_upload"), "title": "Recommandation de carrière"},
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cv_data"] = self.get_cv_data()
        return context

    def get(self, request, *args, **kwargs):
        """Add HTTP Refresh header for automatic redirect."""
        response = super().get(request, *args, **kwargs)
        cv_id = kwargs.get("cv_id")
        redirect_url = reverse("candidate:cv_results", kwargs={"cv_id": cv_id})
        response["Refresh"] = f"{self.redirect_delay_seconds};url={redirect_url}"
        return response
