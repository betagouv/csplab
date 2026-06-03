from typing import Any, Dict, Protocol, Union

from ddd.entity import Entity

from domain.ingestion.entities.document import Document


class ITextExtractor(Protocol):
    def extract_content(self, source: Union[Document, Entity]) -> str: ...

    def extract_metadata(self, source: Union[Document, Entity]) -> Dict[str, Any]: ...
