"""CV upload and confirmation flow views."""

import logging

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
from apps.shared.infrastructure.exceptions import ExternalApiError

logger = logging.getLogger(__name__)


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
        from django.conf import settings

        cv_file = form.cleaned_data["cv_file"]
        logger.info(f"CV upload initiated: filename={cv_file.name}, size={cv_file.size}")

        try:
            pdf_content = cv_file.read()
            container = create_candidate_container()
            process_cv_usecase = container.process_uploaded_cv_usecase()

            cv_id = process_cv_usecase.execute(
                filename=cv_file.name,
                pdf_content=pdf_content,
            )

            logger.info(f"CV processed successfully: cv_id={cv_id}, filename={cv_file.name}")
            messages.success(self.request, "Votre CV a été uploadé avec succès !")
            return redirect("candidate:cv_confirmation", cv_id=cv_id)

        except ExternalApiError as e:
            logger.error(
                f"External API failure: api={e.api_name or 'unknown'}, "
                f"status={e.status_code}, filename={cv_file.name}, error={str(e)}",
                exc_info=not settings.DEBUG  # Full traceback only in prod logs
            )

            if e.status_code in (401, 403):
                user_message = (
                    "Le service d'analyse n'est pas disponible actuellement. "
                    "Veuillez contacter l'administrateur."
                )
            else:
                user_message = (
                    "Le service d'analyse est temporairement indisponible."
                    "Veuillez réessayer dans quelques instants."
                )

            messages.error(self.request, user_message)

            if settings.DEBUG:
                messages.warning(
                    self.request,
                    f"[DEV] API Error: {e.api_name or 'unknown'} - {e.status_code} - {str(e)}"
                )

            return self.form_invalid(form)

        except ValueError as e:
            logger.warning(
                f"Validation error: filename={cv_file.name}, error={str(e)}"
            )
            # Show precise error to user (it's their fault)
            messages.error(self.request, f"Le CV n'a pas pu être traité : {str(e)}")
            return self.form_invalid(form)

        except (ConnectionError, TimeoutError) as e:
            error_type = type(e).__name__
            logger.error(
                f"Network error: type={error_type}, filename={cv_file.name}, error={str(e)}",
                exc_info=True
            )

            user_message = (
                "Le traitement du CV a pris trop de temps. Veuillez réessayer."
                if isinstance(e, TimeoutError)
                else "Problème de connexion au service d'analyse. Veuillez réessayer."
            )
            messages.error(self.request, user_message)

            if settings.DEBUG:
                messages.warning(self.request, f"[DEV] {error_type}: {str(e)}")

            return self.form_invalid(form)

        except Exception as e:
            logger.exception(
                f"Unexpected error processing CV: filename={cv_file.name}, "
                f"error_type={type(e).__name__}, error={str(e)}"
            )

            messages.error(
                self.request,
                "Une erreur inattendue s'est produite. Nos équipes ont été notifiées."
            )

            if settings.DEBUG:
                messages.warning(
                    self.request,
                    f"[DEV] {type(e).__name__}: {str(e)}"
                )

            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submission - USER ERROR."""
        logger.warning(f"Form validation failed: {dict(form.errors)}")

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, str(error))

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
