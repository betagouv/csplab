"""Results and opportunite detail views."""

import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from apps.candidate.container_factory import create_candidate_container
from apps.candidate.infrastructure.adapters.website.fixtures.mock_opportunites import (
    MOCK_OPPORTUNITE_DETAIL,
)
from apps.candidate.infrastructure.adapters.website.views.mixins import (
    BreadcrumbMixin,
    RequiresCVMixin,
)
from apps.shared.infrastructure.exceptions import ExternalApiError
from core.entities.concours import Concours

logger = logging.getLogger(__name__)


class ResultatsAnalyseView(RequiresCVMixin, BreadcrumbMixin, TemplateView):
    """View for CV analysis results page.

    Uses MatchCVToOpportunitiesUsecase to get matching concours.
    The cv_id is passed in the URL and verified by RequiresCVMixin.
    """

    template_name = "candidate/resultats_analyse.html"
    breadcrumb_current = "Résultat de l'analyse"
    breadcrumb_links = []

    def _concours_to_opportunite_dict(self, concours: Concours, score: float) -> dict:
        """Convert Concours entity to opportunite dict for template."""
        return {
            "id": concours.id,
            "title": f"{concours.grade} - {concours.corps}",
            "type": "concours",
            "type_label": ", ".join([m.value for m in concours.access_modality]),
            "location": None,
            "location_display": None,
            "public_service_branch": concours.ministry.value,
            "branch_key": "etat",  # TODO: map ministry to branch_key
            "category": concours.category.value,
            "recruitment_level": concours.category.value,
            "intitule_poste": concours.corps,
            "score": score,
            "written_exam_date": concours.written_exam_date,
            "open_position_number": concours.open_position_number,
            "detail_url": reverse(
                "candidate:opportunite_detail", kwargs={"pk": concours.id}
            ),
        }

    def get_opportunites_filtrees(self, request, cv_id):
        """Get matching opportunites using MatchCVToOpportunitiesUsecase."""
        try:
            container = create_candidate_container()
            match_cv_usecase = container.match_cv_to_opportunities_usecase()

            limit = int(request.GET.get("limit", 20))
            matches = match_cv_usecase.execute(cv_id=str(cv_id), limit=limit)

            opportunites = [
                self._concours_to_opportunite_dict(concours, score)
                for concours, score in matches
            ]

            category = request.GET.get("category", "")
            if category:
                opportunites = [o for o in opportunites if o["category"] == category]

            branches = request.GET.getlist("branch")
            if branches:
                opportunites = [o for o in opportunites if o["branch_key"] in branches]

            logger.info(
                f"Retrieved {len(opportunites)} opportunities for cv_id={cv_id}, "
                f"limit={limit}, filters={{category={category}, branches={branches}}}"
            )
            return opportunites

        except ValueError as e:
            # Validation error (e.g., invalid cv_id) - USER ERROR
            logger.warning(
                f"Validation error fetching opportunities: cv_id={cv_id}, "
                f"error={str(e)}"
            )
            messages.error(request, f"Paramètres invalides : {str(e)}")
            return []

        except ExternalApiError as e:
            logger.error(
                f"External API error fetching opportunities: cv_id={cv_id}, "
                f"api={e.api_name or 'unknown'}, status={e.status_code}, "
                f"error={str(e)}",
                exc_info=not settings.DEBUG,
            )
            messages.error(
                request,
                "Le service de matching est temporairement indisponible. "
                "Veuillez réessayer.",
            )
            if settings.DEBUG:
                messages.warning(request, f"[DEV] API Error: {e.api_name} - {str(e)}")
            return []

        except (ConnectionError, TimeoutError) as e:
            logger.error(
                f"Network error fetching opportunities: cv_id={cv_id}, "
                f"error_type={type(e).__name__}, error={str(e)}",
                exc_info=True,
            )
            messages.error(request, "Problème de connexion. Veuillez réessayer.")
            if settings.DEBUG:
                messages.warning(request, f"[DEV] {type(e).__name__}: {str(e)}")
            return []

        except Exception as e:
            logger.exception(
                f"Unexpected error fetching opportunities: cv_id={cv_id}, "
                f"error_type={type(e).__name__}, error={str(e)}"
            )
            messages.error(
                request,
                "Une erreur s'est produite lors de la récupération des opportunités.",
            )
            if settings.DEBUG:
                messages.warning(request, f"[DEV] {type(e).__name__}: {str(e)}")
            return []

    def get_context_data(self, **kwargs):
        """Add opportunites and filters to context."""
        context = super().get_context_data(**kwargs)
        cv_id = kwargs.get("cv_id")
        context["opportunites"] = self.get_opportunites_filtrees(self.request, cv_id)
        context["cv_data"] = self.get_cv_data()

        context["active_filters"] = {
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
    """

    template_name = "candidate/opportunite_detail.html"
    breadcrumb_current = ""
    breadcrumb_links = []

    def _concours_to_opportunite_detail(self, concours: Concours) -> dict:
        """Convert Concours entity to opportunite detail dict for template."""
        return {
            "id": concours.id,
            "title": f"{concours.grade} - {concours.corps}",
            "type": "concours",
            "type_label": ", ".join([m.value for m in concours.access_modality]),
            "employer": concours.ministry.value,
            "location": None,  # Concours don't have location
            "public_service_branch": concours.ministry.value,
            "branch_key": "etat",  # TODO: map ministry to branch_key
            "category": concours.category.value,
            "recruitment_level": concours.category.value,
            "intitule_poste": concours.corps,
            "description": f"Corps : {concours.corps}\nGrade : {concours.grade}",
            "written_exam_date": concours.written_exam_date,
            "open_position_number": concours.open_position_number,
            "nor_list": [nor.value for nor in concours.nor_list],
            # TODO: add real URL
            "external_url": "https://choisirleservicepublic.gouv.fr/",
        }

    def get_opportunite_data(self, pk):
        """Get opportunite data by ID."""
        try:
            container = create_candidate_container()
            concours_repository = container.shared_container.concours_repository()

            concours = concours_repository.find_by_id(int(pk))
            if concours:
                logger.info(f"Concours found: id={pk}")
                return self._concours_to_opportunite_detail(concours)
            else:
                # Not found - could be user error (bad link) or data issue
                logger.warning(f"Concours not found: id={pk}")
                messages.warning(
                    self.request, "L'opportunité demandée n'existe pas ou plus."
                )
                return MOCK_OPPORTUNITE_DETAIL

        except ValueError as e:
            # Invalid ID format - USER ERROR
            logger.warning(f"Invalid opportunite ID: pk={pk}, error={str(e)}")
            messages.error(self.request, "Identifiant d'opportunité invalide.")
            return MOCK_OPPORTUNITE_DETAIL

        except Exception as e:
            # System error
            logger.exception(
                f"Error fetching opportunite: pk={pk}, "
                f"error_type={type(e).__name__}, error={str(e)}"
            )
            messages.error(
                self.request, "Impossible de charger les détails de cette opportunité."
            )
            if settings.DEBUG:
                messages.warning(self.request, f"[DEV] {type(e).__name__}: {str(e)}")
            return MOCK_OPPORTUNITE_DETAIL

    def get_breadcrumb_data(self):
        """Return breadcrumb data with dynamic current title."""
        pk = self.kwargs.get("pk")
        opportunite = self.get_opportunite_data(pk)
        title = opportunite["title"]
        # Truncate long titles for breadcrumb display
        max_breadcrumb_title_length = 30
        truncated_title = (
            title[:max_breadcrumb_title_length] + "..."
            if len(title) > max_breadcrumb_title_length
            else title
        )
        return {
            "links": self.breadcrumb_links,
            "current": truncated_title,
        }

    def get_context_data(self, **kwargs):
        """Add opportunite to context."""
        context = super().get_context_data(**kwargs)
        pk = kwargs.get("pk")
        context["opportunite"] = self.get_opportunite_data(pk)
        return context
