from enum import Enum


class CVStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
