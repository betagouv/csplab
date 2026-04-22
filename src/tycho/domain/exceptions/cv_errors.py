"""CV domain specific errors."""

from domain.exceptions.domain_errors import DomainError


class CVError(DomainError):
    pass


class InvalidPDFError(CVError):
    def __init__(self, filename: str, reason: str = "Invalid PDF format"):
        self.filename = filename
        self.reason = reason
        super().__init__(f"Invalid PDF file '{filename}': {reason}")


class TextExtractionError(CVError):
    def __init__(self, filename: str, reason: str = "Failed to extract text"):
        self.filename = filename
        self.reason = reason
        super().__init__(f"Text extraction failed for '{filename}': {reason}")


class QueryBuildingError(CVError):
    def __init__(self, reason: str = "Failed to build search query"):
        self.reason = reason
        super().__init__(f"Query building failed: {reason}")


class CVMetadataSaveError(CVError):
    def __init__(self, reason: str = "Failed to save CV metadata"):
        self.reason = reason
        super().__init__(f"CV metadata save failed: {reason}")


class CVNotFoundError(CVError):
    def __init__(self, cv_id: str):
        self.cv_id = cv_id
        super().__init__(f"CV metadata not found for ID: {cv_id}")


class CVProcessingTimeoutError(CVError):
    def __init__(self, cv_id: str, timeout: int):
        self.cv_id = cv_id
        self.timeout = timeout
        super().__init__(f"CV processing timed out for ID: {cv_id} after {timeout}s")


class CVProcessingFailedError(CVError):
    def __init__(self, cv_id: str, reason: str = "Processing failed"):
        self.cv_id = cv_id
        self.reason = reason
        super().__init__(f"CV processing failed for ID: {cv_id}: {reason}")
