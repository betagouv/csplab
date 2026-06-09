from typing import Callable, Protocol, TypeVar
from uuid import UUID

from ddd.aggregate_root import AggregateRoot

AggregateType = TypeVar("AggregateType", bound=AggregateRoot)


class IBaseRepository(Protocol[AggregateType]):
    def get_by_id(self, aggregate_id: UUID) -> AggregateType | None: ...

    def save(self, aggregate: AggregateType) -> None: ...

    def delete(self, aggregate_id: UUID) -> None: ...

    def filter_by(
        self, predicate: Callable[[AggregateType], bool]
    ) -> list[AggregateType]: ...

    def get_all(self) -> list[AggregateType]: ...
