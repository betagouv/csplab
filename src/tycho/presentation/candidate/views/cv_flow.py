import logging
from collections.abc import Sequence
from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.exceptions.offer_errors import OfferDoesNotExist
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.di.candidate.candidate_factory import create_candidate_container
from presentation.candidate.forms.cv_flow import CVUploadForm
from presentation.candidate.mappers import (
    ConcoursToTemplateMapper,
    OfferToTemplateMapper,
    ViewFiltersToUsecaseMapper,
)
from presentation.candidate.mixins import (
    BreadcrumbLink,
    BreadcrumbMixin,
)
from presentation.candidate.presenters import OpportunityListPresenter
from presentation.candidate.tasks import process_cv_task

logger = logging.getLogger(__name__)


class CVUploadView(BreadcrumbMixin, FormView):
    template_name = "candidate/cv_upload.html"
    form_class = CVUploadForm
    breadcrumb_current = "Importer un CV"
    breadcrumb_links: list[BreadcrumbLink] = []
    success_url = reverse_lazy("candidate:cv_upload")  # TODO: change to next step URL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()
        self.logger = self.container.logger_service()

    def form_valid(self, form: CVUploadForm) -> HttpResponse:
        cv_file = form.cleaned_data["cv_file"]
        self.logger.info(
            "CV upload validated: filename=%s, size=%d",
            cv_file.name,
            cv_file.size,
        )

        # Initialize CV metadata
        initialize_cv_metadata_usecase = self.container.initialize_cv_metadata_usecase()
        cv_uuid = initialize_cv_metadata_usecase.execute(cv_file.name)

        # Launch async CV processing
        process_cv_task(cv_uuid, cv_file.read())

        return redirect("candidate:cv_results", cv_uuid=cv_uuid)

    def form_invalid(self, form: CVUploadForm) -> HttpResponse:
        self.logger.warning("Form validation failed: %s", dict(form.errors))
        return super().form_invalid(form)


class CVResultsView(BreadcrumbMixin, TemplateView):
    breadcrumb_current = "Résultat de l'analyse"
    breadcrumb_links: list[BreadcrumbLink] = [
        {"url": reverse_lazy("candidate:cv_upload"), "title": "Importer un CV"},
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()
        self._filters_mapper = ViewFiltersToUsecaseMapper()
        self._status: CVStatus = CVStatus.PENDING
        self._filename: str | None = None
        self._opportunities: Sequence[tuple[Concours | Offer, float]] = []

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        cv_uuid: UUID = kwargs["cv_uuid"]
        self._fetch_cv_data(request, cv_uuid)

        presenter = OpportunityListPresenter(self._opportunities, request)
        is_htmx = bool(request.headers.get("HX-Request"))

        if is_htmx and request.GET.get("poll") and self._status != CVStatus.PENDING:
            response = HttpResponse()
            response["HX-Redirect"] = str(
                reverse_lazy("candidate:cv_results", kwargs={"cv_uuid": cv_uuid})
            )
            return response

        match self._status:
            case CVStatus.PENDING:
                return self._handle_pending(request, is_htmx, **kwargs)
            case CVStatus.FAILED:
                return self._handle_failed(request, is_htmx)
            case CVStatus.COMPLETED if not presenter.cards:
                return self._handle_no_results(request, is_htmx, presenter, **kwargs)
            case _:
                return self._handle_completed(request, is_htmx, presenter, **kwargs)

    def _fetch_cv_data(self, request, cv_uuid: UUID) -> None:
        cv_metadata_repo = self.container.postgres_cv_metadata_repository()
        try:
            cv_metadata = cv_metadata_repo.find_by_id(cv_uuid)
        except Exception:
            self._status = CVStatus.FAILED
            return

        if cv_metadata is None:
            self._status = CVStatus.FAILED
            return

        self._status = cv_metadata.status
        self._filename = cv_metadata.filename

        if cv_metadata.status != CVStatus.COMPLETED or not cv_metadata.search_query:
            return

        try:
            usecase = self.container.match_cv_to_opportunities_usecase()
            domain_filters = self._filters_mapper.to_domain(request.GET)
            self._opportunities = usecase.execute(
                cv_metadata=cv_metadata,
                filters=domain_filters,
                limit=settings.CV_MAX_OPPORTUNITIES,
            )
        except Exception:
            self._status = CVStatus.FAILED

    def _handle_pending(self, request, is_htmx: bool, **kwargs) -> HttpResponse:
        if is_htmx:
            response = HttpResponse(status=204)
            response["HX-Reswap"] = "none"
            return response

        context = self._base_context(**kwargs)
        return render(request, "candidate/cv_processing.html", context)

    def _handle_failed(self, request, is_htmx: bool) -> HttpResponse:
        messages.error(
            request,
            "Une erreur est survenue lors du traitement de votre CV. "
            "Veuillez réessayer.",
        )
        if is_htmx:
            response = HttpResponse()
            response["HX-Redirect"] = str(reverse_lazy("candidate:cv_upload"))
            return response
        return redirect("candidate:cv_upload")

    def _handle_no_results(
        self,
        request,
        is_htmx: bool,
        presenter: OpportunityListPresenter,
        **kwargs,
    ) -> HttpResponse:
        context = self._base_context(**kwargs)
        context["cv_name"] = self._filename
        context["tally_form_id"] = settings.TALLY_FORM_ID_NO_RESULTS
        context.update(presenter.get_filter_options())

        template = (
            "candidate/components/_no_results_content.html"
            if is_htmx
            else "candidate/cv_no_results.html"
        )
        return render(request, template, context)

    def _handle_completed(
        self,
        request,
        is_htmx: bool,
        presenter: OpportunityListPresenter,
        **kwargs,
    ) -> HttpResponse:
        context = self._base_context(**kwargs)
        context["cv_name"] = self._filename
        context["tally_form_id"] = settings.TALLY_FORM_ID_RESULTS
        context.update(presenter.get_paginated_context())
        context.update(presenter.get_filter_options())
        context["results_target_id"] = "results-zone"

        hx_target = request.headers.get("HX-Target")
        if is_htmx:
            template = (
                "candidate/components/_results_list.html"
                if hx_target == "results-zone"
                else "candidate/components/_results_content.html"
            )
        else:
            template = "candidate/cv_results.html"

        return render(request, template, context)

    def _base_context(self, **kwargs) -> dict[str, object]:
        context: dict[str, object] = {
            "breadcrumb_data": self.get_breadcrumb_data(),
            "cv_uuid": kwargs.get("cv_uuid"),
            "poll_interval": settings.CV_PROCESSING_POLL_INTERVAL,
        }
        return context

    def get_breadcrumb_context(self) -> dict[str, object]:
        return self.get_breadcrumb_data()


class OfferDrawerView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/components/_opportunity_drawer.html"
    breadcrumb_current = "Détail de l'offre"

    def get_breadcrumb_data(self) -> dict:
        cv_uuid = self.kwargs.get("cv_uuid")
        return {
            "links": [
                {"url": reverse_lazy("candidate:cv_upload"), "title": "Importer un CV"},
                {
                    "url": reverse_lazy(
                        "candidate:cv_results", kwargs={"cv_uuid": cv_uuid}
                    ),
                    "title": "Résultat de l'analyse",
                },
            ],
            "current": self.breadcrumb_current,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["candidate/components/_opportunity_drawer.html"]
        return ["candidate/opportunity_detail.html"]

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        offer_id = self.kwargs.get("offer_id")

        offers_repository = self.container.offers_repository()
        try:
            offer = offers_repository.find_by_id(offer_id)
            context["opportunity"] = OfferToTemplateMapper.map_for_drawer(offer)
        except OfferDoesNotExist:
            raise Http404("Offer not found") from None

        context["cv_uuid"] = self.kwargs.get("cv_uuid")
        return context


class ConcoursDrawerView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/components/_opportunity_drawer.html"
    breadcrumb_current = "Détail du concours"

    def get_breadcrumb_data(self) -> dict:
        cv_uuid = self.kwargs.get("cv_uuid")
        return {
            "links": [
                {"url": reverse_lazy("candidate:cv_upload"), "title": "Importer un CV"},
                {
                    "url": reverse_lazy(
                        "candidate:cv_results", kwargs={"cv_uuid": cv_uuid}
                    ),
                    "title": "Résultat de l'analyse",
                },
            ],
            "current": self.breadcrumb_current,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["candidate/components/_opportunity_drawer.html"]
        return ["candidate/opportunity_detail.html"]

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        concours_id = self.kwargs.get("concours_id")

        concours_repository = self.container.concours_repository()
        try:
            concours = concours_repository.find_by_id(concours_id)
            context["opportunity"] = ConcoursToTemplateMapper.map_for_drawer(concours)
        except ConcoursDoesNotExist:
            raise Http404("Concours not found") from None

        context["cv_uuid"] = self.kwargs.get("cv_uuid")
        return context
