"""Mapping layer for /api/v2/offersummaries.

Target internal format:
{
  "offers": [
     {
       "id": "...",              # reference
       "title": "...",           # offerFamilyCategory.label
       "profile": "...",         # title
       "category": "",           # placeholder
       "verse": "...",           # salaryRange.clientCode
       "region": "...",          # region.label
       "department": "...",      # department.label
       "limit_date": ""          # placeholder
     }
  ]
}
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, TypedDict, cast

from ..dtos.talentsoft_offer_summary_dto import TalentSoftOfferDocument

logger = logging.getLogger(__name__)


class Referential(TypedDict, total=False):
    """TalentSoft referential object shape (partial)."""

    label: str
    clientCode: str


class OfferSummary(TypedDict, total=False):
    """TalentSoft offersummaries item shape (partial)."""

    reference: str
    title: str
    offerFamilyCategory: Referential
    salaryRange: Referential

    # In practice these can be dict OR list[dict] (or empty list)
    region: Referential | List[Referential]
    department: Referential | List[Referential]

    # Depending on tenant/API version, deadline can be exposed with different keys.
    # Keep these typed as optional strings.
    limitDate: str
    limit_date: str
    endPublicationDate: str
    endPublicationDateUtc: str


class OfferSummariesPayload(TypedDict, total=False):
    """TalentSoft offersummaries payload shape (partial)."""

    data: List[OfferSummary]


class OfferSummariesMapper:
    """Convert TalentSoft offersummaries payload to internal offers schema."""

    @staticmethod
    def _extract_label(value: Referential | List[Referential] | Any) -> str:
        """Extract first available 'label' from dict or list[dict]."""
        if isinstance(value, dict):
            return str(value.get("label") or "")
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, dict):
                return str(first.get("label") or "")
        return ""

    @staticmethod
    def _extract_client_code(value: Referential | Any) -> str:
        """Extract clientCode safely from a referential dict."""
        if isinstance(value, dict):
            return str(value.get("clientCode") or "")
        return ""

    @staticmethod
    def _require_non_empty(value: str, field_name: str) -> str:
        """Return stripped value or raise if empty."""
        v = (value or "").strip()
        if not v:
            raise ValueError(f"Missing required field '{field_name}'")
        return v

    @classmethod
    def _extract_limit_date(cls, item: OfferSummary) -> str:
        """Extract limit date from known keys.

        NOTE: adjust the key precedence if your API uses a specific field name.
        """
        candidates = [
            item.get("limitDate"),
            item.get("limit_date"),
            item.get("endPublicationDate"),
            item.get("endPublicationDateUtc"),
        ]
        for c in candidates:
            if isinstance(c, str) and c.strip():
                return c.strip()
        return ""

    @classmethod
    def map_item(cls, item: OfferSummary) -> TalentSoftOfferDocument:
        """Map one offersummary item to TalentSoftOfferDocument (strict required fields)."""
        # Required core fields
        offer_id = cls._require_non_empty(str(item.get("reference") or ""), "id")
        profile = cls._require_non_empty(str(item.get("title") or ""), "profile")

        title = cls._require_non_empty(
            cls._extract_label(item.get("offerFamilyCategory")),
            "title",
        )
        verse = cls._require_non_empty(
            cls._extract_client_code(item.get("salaryRange")),
            "verse",
        )

        # Required business fields
        region = cls._require_non_empty(
            cls._extract_label(item.get("region")), "region"
        )
        department = cls._require_non_empty(
            cls._extract_label(item.get("department")), "department"
        )
        limit_date = cls._require_non_empty(cls._extract_limit_date(item), "limit_date")

        return TalentSoftOfferDocument(
            id=offer_id,
            title=title,
            profile=profile,
            category="",  # TODO: filled later by another API call (known business decision)
            verse=verse,
            region=region,
            department=department,
            limit_date=limit_date,
        )

    @classmethod
    def map_payload(cls, payload: OfferSummariesPayload) -> Dict[str, List[dict]]:
        """Map full payload into {'offers': [...]}.

        - strict mapping (required fields enforced)
        - logs + skips invalid offers (prod-safe)
        """
        data = payload.get("data", [])
        offers: List[dict] = []

        if not isinstance(data, list):
            logger.warning("Skipping payload: 'data' is not a list (%s)", type(data))
            return {"offers": offers}

        for i, raw in enumerate(data):
            if not isinstance(raw, dict):
                logger.warning("Skipping non-dict offer at index %s: %s", i, type(raw))
                continue
            try:
                doc = cls.map_item(cast(OfferSummary, raw))
                offers.append(doc.model_dump())
            except Exception as exc:
                logger.warning(
                    "Skipping invalid offer at index %s: %s", i, exc, exc_info=True
                )

        return {"offers": offers}
