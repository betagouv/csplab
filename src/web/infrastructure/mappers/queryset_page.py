from typing import Generic, TypeVar

from ddd.mapper_interface import IToDomainMapper
from ddd.page_interface import IPage

T = TypeVar("T")
Q = TypeVar("Q")


class QuerySetPage(IPage[T], Generic[T]):
    def __init__(self, qs):
        self._qs = qs

    def count(self) -> int:
        return self._qs.count()

    def slice(self, offset, limit):
        sliced_qs = self._qs[offset : offset + limit]
        return (m.to_entity() for m in sliced_qs)


class QuerySetPageMapper(IPage[Q], Generic[Q]):
    def __init__(self, qs, mapper: IToDomainMapper) -> None:
        self._qs = qs
        self._mapper = mapper

    def count(self) -> int:
        return self._qs.count()

    def slice(self, offset, limit):
        return (self._mapper.to_domain(m) for m in self._qs[offset : offset + limit])
