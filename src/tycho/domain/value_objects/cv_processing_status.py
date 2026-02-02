"""Status enumeration for CV processing."""

from enum import Enum


class CVStatus(Enum):
    """Status enumeration for CV processing."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
