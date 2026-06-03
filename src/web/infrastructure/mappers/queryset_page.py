from typing import Generic, TypeVar

from ddd.page_interface import IPage

T = TypeVar("T")


class QuerySetPage(IPage[T], Generic[T]):
    def __init__(self, qs):
        self._qs = qs

    def count(self) -> int:
        return self._qs.count()

    def slice(self, offset, limit):
        sliced_qs = self._qs[offset : offset + limit]
        return (m.to_entity() for m in sliced_qs)
