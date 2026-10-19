from uuid import UUID

from ddd.domain_errors import DomainError


class VectorDeletionError(DomainError):
    def __init__(self, entity_ids: list[UUID]):
        self.entity_ids = entity_ids
        super().__init__(f"Failed to delete vectorized document(s): {entity_ids}")
