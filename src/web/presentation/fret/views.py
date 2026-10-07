import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.views.generic import DetailView, ListView

from application.ingestion.errors.application_errors_ingestion import (
    AccesSourcesRefuse,
    OffreIntrouvable,
    SourceNonAutorisee,
)
from application.ingestion.services.get_offer_by_source import get_offer_by_source
from application.ingestion.services.list_authorized_sources import (
    list_authorized_sources,
)
from application.ingestion.services.list_offers_by_source import list_offers_by_source
from config.logger_names import LoggerName
from presentation.fret.offre_rows import offre_rows

logger = logging.getLogger(LoggerName.INGESTION.value)

PAGINATE_BY = 50


class SourceListView(LoginRequiredMixin, ListView):
    template_name = "fret/sources.html"
    context_object_name = "sources"
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        try:
            return list_authorized_sources(self.request.user)
        except AccesSourcesRefuse as e:
            logger.warning("%s", e)
            raise PermissionDenied from e

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
        context["breadcrumb_data"] = {"current": "Mes sources"}
        return context


class SourceFromUrlMixin:
    @cached_property
    def source(self):
        try:
            return get_object_or_404(
                list_authorized_sources(self.request.user),
                source_id=self.kwargs["source_id"],
            )
        except AccesSourcesRefuse as e:
            logger.warning("%s", e)
            raise PermissionDenied from e
        except Http404:
            logger.warning(
                "Source %s introuvable ou non autorisée pour l'utilisateur %s",
                self.kwargs["source_id"],
                self.request.user.username,
            )
            raise


class OffreListView(LoginRequiredMixin, SourceFromUrlMixin, ListView):
    template_name = "fret/offres.html"
    context_object_name = "offres"
    paginate_by = PAGINATE_BY

    @cached_property
    def search(self):
        return self.request.GET.get("q", "").strip()

    def get_queryset(self):
        try:
            return list_offers_by_source(
                self.request.user, self.source.source_id, self.search
            )
        except SourceNonAutorisee as e:
            logger.warning(
                "Accès refusé à la source %s pour l'utilisateur %s",
                self.source.source_id,
                self.request.user.username,
            )
            raise PermissionDenied from e

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            source=self.source,
            search=self.search,
            breadcrumb_data={
                "links": [{"url": reverse("fret:sources"), "title": "Mes sources"}],
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


class OffreDetailView(LoginRequiredMixin, SourceFromUrlMixin, DetailView):
    template_name = "fret/offre_detail.html"
    context_object_name = "offre"

    def get_object(self, queryset=None):
        try:
            return get_offer_by_source(
                self.request.user, self.source.source_id, self.kwargs["offre_id"]
            )
        except SourceNonAutorisee as e:
            logger.warning(
                "Accès refusé à la source %s pour l'utilisateur %s",
                self.source.source_id,
                self.request.user.username,
            )
            raise PermissionDenied from e
        except OffreIntrouvable as e:
            logger.warning(
                "Offre %s introuvable dans la source %s pour l'utilisateur %s",
                self.kwargs["offre_id"],
                self.source.source_id,
                self.request.user.username,
            )
            raise Http404 from e

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offre = context["offre"]
        context.update(
            source=self.source,
            breadcrumb_data={
                "links": [
                    {"url": reverse("fret:sources"), "title": "Mes sources"},
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
