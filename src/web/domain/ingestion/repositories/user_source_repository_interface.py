from typing import Any, Protocol
from uuid import UUID


class IUserSourceRepository(Protocol):
    def get_allowed_source_ids(self, user: Any, source_ids: set[UUID]) -> set[UUID]: ...
