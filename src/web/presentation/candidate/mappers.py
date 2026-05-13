from typing import Any

from django.http import QueryDict
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from domain.entities.concours import Concours
from domain.entities.document import DocumentType
from domain.entities.offer import Offer
from domain.interfaces.mapper_interface import IToDomainMapper
from domain.repositories.vector_repository_interface import IFilters
from domain.value_objects.category import Category
from domain.value_objects.department import Department
from domain.value_objects.opportunity_type import OpportunityType
from domain.value_objects.verse import Verse
from presentation.candidate.filter_config import (
    CATEGORY_FILTER_VALUE,
    FILTER_PARAM_CATEGORY,
    FILTER_PARAM_LOCATION,
    FILTER_PARAM_OPPORTUNITY_TYPE,
    FILTER_PARAM_VERSANT,
    format_category_value,
    format_location_value,
)
from presentation.candidate.formatters import (
    format_category_display,
    format_contract_type_display,
    format_location_display,
    format_opportunity_type_display,
    format_verse_display,
)
from presentation.candidate.types import (
    AccordionItem,
    ConcoursCard,
    DrawerContext,
    OfferCard,
)


class ConcoursToTemplateMapper:
    @staticmethod
    def map_for_card(concours: Concours) -> ConcoursCard:
        return {
            "opportunity_type": OpportunityType.CONCOURS,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.CONCOURS
            ),
            "concours_id": str(concours.id),
            "title": concours.corps,
            "description": concours.grade,
            "ministry": str(concours.ministry),
            "access_modalities": [str(m) for m in concours.access_modality]
            if concours.access_modality
            else [],
            "category_display": format_category_display(concours.category),
            "category_value": format_category_value(concours.category),
            "versant_display": format_verse_display(Verse.FPE),
            "versant_value": Verse.FPE.value,
            "url": "#",
        }

    @staticmethod
    def map_for_drawer(concours: Concours) -> DrawerContext:
        accordions: list[AccordionItem] = []
        if concours.grade:
            accordions.append(
                {
                    "id": "drawer-grade-content",
                    "title": "Grade",
                    "content": mark_safe(  # noqa: S308
                        linebreaks(concours.grade, autoescape=True)
                    ),
                }
            )
        return {
            "title": concours.corps,
            "opportunity_id": str(concours.id),
            "opportunity_type": OpportunityType.CONCOURS,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.CONCOURS
            ),
            "versant_display": format_verse_display(Verse.FPE),
            "category_display": format_category_display(concours.category),
            "ministry": str(concours.ministry),
            "url": "#",
            "accordions": accordions,
            "cta_label": "Voir le concours",
        }


class OfferToTemplateMapper:
    @staticmethod
    def map_for_card(offer: Offer) -> OfferCard:
        return {
            "opportunity_type": OpportunityType.OFFER,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.OFFER
            ),
            "title": offer.title,
            "description": offer.mission,
            "offer_id": str(offer.id),
            "profile": offer.profile,
            "organization": offer.organization,
            "category_display": format_category_display(offer.category),
            "category_value": format_category_value(offer.category),
            "versant_display": format_verse_display(offer.verse),
            "versant_value": offer.verse.value if offer.verse else "",
            "location": format_location_display(offer.localisation),
            "location_value": format_location_value(offer.localisation),
            "contract_type_display": format_contract_type_display(offer.contract_type),
            "url": str(offer.offer_url) if offer.offer_url else "#",
        }

    @staticmethod
    def map_for_drawer(offer: Offer) -> DrawerContext:
        accordions: list[AccordionItem] = []
        if offer.mission:
            accordions.append(
                {
                    "id": "drawer-mission-content",
                    "title": "Mission",
                    "content": mark_safe(  # noqa: S308
                        linebreaks(offer.mission, autoescape=True)
                    ),
                }
            )
        if offer.profile:
            accordions.append(
                {
                    "id": "drawer-profile-content",
                    "title": "Profil recherch\u00e9",
                    "content": mark_safe(  # noqa: S308
                        linebreaks(offer.profile, autoescape=True)
                    ),
                }
            )
        return {
            "title": offer.title,
            "opportunity_id": str(offer.id),
            "opportunity_type": OpportunityType.OFFER,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.OFFER
            ),
            "versant_display": format_verse_display(offer.verse),
            "category_display": format_category_display(offer.category),
            "organization": offer.organization,
            "location": format_location_display(offer.localisation),
            "url": str(offer.offer_url) if offer.offer_url else "#",
            "accordions": accordions,
            "cta_label": "Voir l'offre",
        }


class ViewFiltersToUsecaseMapper(IToDomainMapper[QueryDict, IFilters]):
    def to_domain(self, view_filters: QueryDict | None) -> IFilters:
        if not view_filters:
            return {}
        usecase_filters: dict[str, Any] = {}

        self._map_departments(view_filters, usecase_filters)
        self._map_categories(view_filters, usecase_filters)
        self._map_versants(view_filters, usecase_filters)
        self._map_opportunity_types(view_filters, usecase_filters)

        return usecase_filters

    def _map_departments(
        self, view_filters: QueryDict, usecase_filters: dict[str, Any]
    ) -> None:
        departments = view_filters.getlist(FILTER_PARAM_LOCATION)
        if not departments:
            return
        department_objects = [
            Department(code=dept_code.strip())
            for dept_code in departments
            if dept_code and dept_code.strip()
        ]
        if not department_objects:
            return
        usecase_filters["department"] = department_objects

    def _map_categories(
        self, view_filters: QueryDict, usecase_filters: dict[str, Any]
    ) -> None:
        categories = view_filters.getlist(FILTER_PARAM_CATEGORY)
        if not categories:
            return
        value_to_categories: dict[str, list[Category]] = {}
        for category, value in CATEGORY_FILTER_VALUE.items():
            if value not in value_to_categories:
                value_to_categories[value] = []
            value_to_categories[value].append(category)

        mapped_categories = []
        for cat_value in categories:
            if cat_value in value_to_categories:
                mapped_categories.extend(value_to_categories[cat_value])
        if not mapped_categories:
            return
        usecase_filters["category"] = mapped_categories

    def _map_versants(
        self, view_filters: QueryDict, usecase_filters: dict[str, Any]
    ) -> None:
        versants = view_filters.getlist(FILTER_PARAM_VERSANT)
        if not versants:
            return
        verse_objects = [
            Verse(versant)
            for versant in versants
            if versant in [v.value for v in Verse]
        ]
        if not verse_objects:
            return
        usecase_filters["verse"] = verse_objects

    def _map_opportunity_types(
        self, view_filters: QueryDict, usecase_filters: dict[str, Any]
    ) -> None:
        opportunity_types = view_filters.getlist(FILTER_PARAM_OPPORTUNITY_TYPE)
        if not opportunity_types:
            return
        type_mapping = {
            "offer": DocumentType.OFFERS,
            "concours": DocumentType.CONCOURS,
        }
        doc_type_objects = [
            type_mapping[doc_type]
            for doc_type in opportunity_types
            if doc_type in type_mapping
        ]
        if not doc_type_objects:
            return
        usecase_filters["document_type"] = doc_type_objects
