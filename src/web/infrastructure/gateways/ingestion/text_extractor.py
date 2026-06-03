from typing import Any, Dict, Union

from ddd.entity import Entity
from referentiel.entities.concours import Concours
from referentiel.entities.corps import Corps
from referentiel.entities.metier import Metier
from referentiel.entities.offer import Offer

from domain.ingestion.entities.document import Document
from domain.ingestion.services.text_extractor_interface import ITextExtractor


class TextExtractor(ITextExtractor):
    def extract_content(self, source: Union[Document, Entity]) -> str:
        if isinstance(source, Corps):
            return self._extract_from_corps(source)
        elif isinstance(source, Concours):
            return self._extract_from_concours(source)
        elif isinstance(source, Offer):
            return self._extract_from_offer(source)
        elif isinstance(source, Metier):
            return self._extract_from_metier(source)
        else:
            raise NotImplementedError(
                f"Content extraction not implemented for {type(source)}"
            )

    def extract_metadata(self, source: Union[Document, Entity]) -> Dict[str, Any]:
        if isinstance(source, Corps):
            return self._extract_metadata_from_corps(source)
        elif isinstance(source, Concours):
            return self._extract_metadata_from_concours(source)
        elif isinstance(source, Offer):
            return self._extract_metadata_from_offer(source)
        elif isinstance(source, Metier):
            return self._extract_metadata_from_metier(source)
        else:
            raise NotImplementedError(
                f"Metadata extraction not implemented for {type(source)}"
            )

    def _extract_from_corps(self, corps: Corps) -> str:
        return corps.label.value

    def _extract_metadata_from_document(self, document: Document) -> Dict[str, Any]:
        raise NotImplementedError(
            f"Metadata extraction not implemented for document type {document.type}"
        )

    def _extract_metadata_from_corps(self, corps: Corps) -> Dict[str, Any]:
        return {
            "category": corps.category.value if corps.category else None,
            "access_mod": [am.value for am in corps.access_modalities],
            "ministry": corps.ministry.value,
        }

    def _extract_from_concours(self, concours: Concours) -> str:
        return f"{concours.corps} {concours.grade}".strip()

    def _extract_metadata_from_concours(self, concours: Concours) -> Dict[str, Any]:
        return {
            "category": concours.category.value,
            "ministry": concours.ministry.value,
            "access_modality": [am.value for am in concours.access_modality],
        }

    def _extract_from_offer(self, offer: Offer) -> str:
        return f"{offer.title}"

    def _extract_metadata_from_offer(self, offer: Offer) -> Dict[str, Any]:
        localisation_data = None
        if offer.localisation:
            localisation_data = {
                "country": offer.localisation.country,
                "region": offer.localisation.region.code,
                "department": offer.localisation.department.code,
            }

        return {
            "category": offer.category.value if offer.category else None,
            "verse": offer.verse.value if offer.verse else None,
            "localisation": localisation_data,
        }

    def _extract_from_metier(self, metier: Metier) -> str:
        return f"{metier.libelle}"

    def _extract_metadata_from_metier(self, metier: Metier) -> Dict[str, Any]:
        return {
            "versants": metier.versants,
        }
