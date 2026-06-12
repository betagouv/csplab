from uuid import UUID

from ddd.domain_errors import DomainError


class SourceAuthorizationError(DomainError):
    def __init__(self, source_ids: set[UUID]):
        self.source_ids = source_ids
        super().__init__(f"Not authorized to access source(s): {source_ids}")
