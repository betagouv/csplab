from collections.abc import Sequence

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest
from dsfr.utils import list_pages

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.value_objects.opportunity_type import OpportunityType
from presentation.candidate.filter_config import (
    get_all_departments_filter_options,
    get_category_filter_options,
    get_opportunity_type_filter_options,
    get_verse_filter_options,
)
from presentation.candidate.mappers import (
    ConcoursToTemplateMapper,
    OfferToTemplateMapper,
)
from presentation.candidate.types import FilterOption, OpportunityCard


class OpportunityListPresenter:
    def __init__(
        self,
        raw_opportunities: Sequence[tuple[Concours | Offer, float]],
        request: HttpRequest,
    ) -> None:
        self._raw_opportunities = raw_opportunities
        self._request = request
        self._cards: list[OpportunityCard] | None = None

    @property
    def cards(self) -> list[OpportunityCard]:
        if self._cards is None:
            self._cards = self._map_to_cards()
        return self._cards

    def _map_to_cards(self) -> list[OpportunityCard]:
        result: list[OpportunityCard] = []
        for entity, _score in self._raw_opportunities:
            if isinstance(entity, Concours):
                result.append(ConcoursToTemplateMapper.map_for_card(entity))
            elif isinstance(entity, Offer):
                result.append(OfferToTemplateMapper.map_for_card(entity))
        return result

    def get_paginated_context(self) -> dict[str, object]:
        filtered = self.cards
        paginator = Paginator(filtered, settings.CV_RESULTS_PER_PAGE)
        page_obj = paginator.get_page(self._request.GET.get("page", 1))
        list_pages(page_obj)
        return {
            "results": page_obj.object_list,
            "results_count": len(filtered),
            "page_obj": page_obj,
        }

    def get_filter_options(self) -> dict[str, object]:
        params = self._request.GET
        return {
            "location_options": self._mark_checked(
                get_all_departments_filter_options(),
                params.getlist("filter-location"),
            ),
            "category_options": self._mark_checked(
                get_category_filter_options(),
                params.getlist("filter-category"),
            ),
            "verse_options": self._mark_checked(
                get_verse_filter_options(),
                params.getlist("filter-versant"),
            ),
            "opportunity_type_options": self._mark_checked(
                get_opportunity_type_filter_options(),
                params.getlist("filter-opportunity_type"),
            ),
            "opportunity_type_offer": OpportunityType.OFFER,
            "opportunity_type_concours": OpportunityType.CONCOURS,
        }

    @staticmethod
    def _mark_checked(
        options: list[FilterOption],
        active_values: list[str],
    ) -> list[FilterOption]:
        if not active_values:
            return options
        active_set = set(active_values)
        return [
            FilterOption(
                value=opt["value"],
                text=opt["text"],
                checked=opt["value"] in active_set,
            )
            for opt in options
        ]
