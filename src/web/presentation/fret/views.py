import logging

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.views.generic import DetailView, ListView

from application.ingestion.errors.application_errors_ingestion import (
    OffreIntrouvable,
    SourceIntrouvable,
)
from application.ingestion.services.get_offer_by_source import get_offer_by_source
from application.ingestion.services.list_offers_by_source import list_offers_by_source
from application.ingestion.services.list_sources import list_sources
from config.logger_names import LoggerName
from presentation.fret.offre_rows import offre_rows

logger = logging.getLogger(LoggerName.INGESTION.value)

PAGINATE_BY = 50


class FretEnabledMixin:
    def dispatch(self, request, *args, **kwargs):
        if not settings.FRET_ENABLED:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class SourceListView(FretEnabledMixin, ListView):
    template_name = "fret/sources.html"
    context_object_name = "sources"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return list_sources()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = {
            "header": ["Source", "Type"],
            "content": [
                [
                    format_html(
                        '<a href="{}">{}</a>',
                        reverse("fret:offres", args=[source.source_id]),
                        source.slug,
                    ),
                    format_html("{}", source.type),
                ]
                for source in context["sources"]
            ],
        }
        context["breadcrumb_data"] = {"current": "Sources"}
        return context


class SourceFromUrlMixin:
    @cached_property
    def source(self):
        try:
            return get_object_or_404(list_sources(), source_id=self.kwargs["source_id"])
        except Http404:
            logger.warning("Source %s introuvable", self.kwargs["source_id"])
            raise


class OffreListView(FretEnabledMixin, SourceFromUrlMixin, ListView):
    template_name = "fret/offres.html"
    context_object_name = "offres"
    paginate_by = PAGINATE_BY

    @cached_property
    def search(self):
        return self.request.GET.get("q", "").strip()

    def get_queryset(self):
        try:
            return list_offers_by_source(self.source.source_id, self.search)
        except SourceIntrouvable as e:
            logger.warning("%s", e)
            raise Http404 from e

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            source=self.source,
            search=self.search,
            breadcrumb_data={
                "links": [{"url": reverse("fret:sources"), "title": "Sources"}],
                "current": self.source.slug,
            },
            table={
                "header": ["Référence", "Titre", "Organisme", "Publication"],
                "content": [
                    [
                        format_html(
                            '<a href="{}">{}</a>',
                            reverse(
                                "fret:offre", args=[self.source.source_id, offre.pk]
                            ),
                            offre.reference,
                        ),
                        format_html("{}", offre.title),
                        format_html("{}", offre.organization),
                        format_html("{}", offre.publication_date.strftime("%d/%m/%Y")),
                    ]
                    for offre in context["offres"]
                ],
            },
        )
        return context


class OffreDetailView(FretEnabledMixin, SourceFromUrlMixin, DetailView):
    template_name = "fret/offre_detail.html"
    context_object_name = "offre"

    def get_object(self, queryset=None):
        try:
            return get_offer_by_source(self.source.source_id, self.kwargs["offre_id"])
        except SourceIntrouvable as e:
            logger.warning("%s", e)
            raise Http404 from e
        except OffreIntrouvable as e:
            logger.warning(
                "Offre %s introuvable dans la source %s",
                self.kwargs["offre_id"],
                self.source.source_id,
            )
            raise Http404 from e

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offre = context["offre"]
        context.update(
            source=self.source,
            breadcrumb_data={
                "links": [
                    {"url": reverse("fret:sources"), "title": "Sources"},
                    {
                        "url": reverse("fret:offres", args=[self.source.source_id]),
                        "title": self.source.slug,
                    },
                ],
                "current": offre.reference,
            },
            table={
                "caption": "Données de l'offre",
                "content": offre_rows(offre),
            },
        )
        return context
