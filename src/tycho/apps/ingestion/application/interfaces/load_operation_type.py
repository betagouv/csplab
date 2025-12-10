"""Load operation type value object."""

from enum import Enum


class LoadOperationType(Enum):
    """Types of load operations for documents."""

    FETCH_FROM_API = "FETCH_FROM_API"
    UPLOAD_FROM_CSV = "UPLOAD_FROM_CSV"
