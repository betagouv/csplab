"""Load documents input interface."""

from dataclasses import dataclass
from typing import List, Optional

from domain.entities.document import Document, DocumentType


@dataclass
class LoadDocumentsInput:
    """Input for loading documents."""

    document_type: DocumentType
    documents: Optional[List[Document]] = None
