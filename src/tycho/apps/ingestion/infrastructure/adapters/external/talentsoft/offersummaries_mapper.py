"""
Mapping layer for /api/v2/offersummaries.

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

from typing import Any, Dict, List, Optional

from ..dtos.talentsoft_offer_summary_dto import TalentSoftOfferDocument


class OfferSummariesMapper:
    """Convert TalentSoft offersummaries payload to internal offers schema."""

    @staticmethod
    def _extract_label(value: Any) -> str:
        """
        TalentSoft sometimes returns referentials as dicts or lists of dicts.
        We extract the first available 'label'.
        """
        if isinstance(value, dict):
            return str(value.get("label") or "")
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, dict):
                return str(first.get("label") or "")
        return ""

    @staticmethod
    def _extract_client_code(value: Any) -> str:
        """Extract clientCode safely from a dict referential."""
        if isinstance(value, dict):
            return str(value.get("clientCode") or "")
        return ""

    @staticmethod
    def _none_if_empty(value: str) -> Optional[str]:
        """Return None if value is empty/blank; otherwise the stripped value."""
        v = (value or "").strip()
        return v if v else None

    @classmethod
    def map_item(cls, item: Dict[str, Any]) -> TalentSoftOfferDocument:
        """Map one offersummary item to TalentSoftOfferDocument."""
        region_label = cls._extract_label(item.get("region"))
        department_label = cls._extract_label(item.get("department"))

        return TalentSoftOfferDocument(
            id=str(item.get("reference") or ""),
            title=cls._extract_label(item.get("offerFamilyCategory")),
            profile=str(item.get("title") or ""),
            category="",  # TODO: will be filled later via another API call
            verse=cls._extract_client_code(item.get("salaryRange")),
            region=cls._none_if_empty(region_label),
            department=cls._none_if_empty(department_label),
            limit_date=None,  # TODO: will be filled later via another API call
        )

    @classmethod
    def map_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Map full payload into {'offers': [...]}."""
        data = payload.get("data") or []
        if not isinstance(data, list):
            data = []

        offers: List[Dict[str, Any]] = []
        for raw in data:
            if isinstance(raw, dict):
                doc = cls.map_item(raw)
                offers.append(doc.model_dump())

        return {"offers": offers}
