"""Input data structure for LoadDocuments usecase."""

from dataclasses import dataclass
from typing import Any, Dict

from apps.ingestion.application.interfaces.load_operation_type import LoadOperationType


@dataclass
class LoadDocumentsInput:
    """Input data for LoadDocuments usecase."""

    operation_type: LoadOperationType
    kwargs: Dict[str, Any]
