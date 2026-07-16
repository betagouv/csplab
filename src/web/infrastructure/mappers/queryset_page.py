from typing import Callable, Generic, TypeVar

from ddd.page_interface import IPage

T = TypeVar("T")


class QuerySetPage(IPage[T], Generic[T]):
    def __init__(self, qs, mapper: Callable):
        self._qs = qs
        self._mapper = mapper

    def count(self) -> int:
        return self._qs.count()

    def slice(self, offset: int, limit: int):
        sliced_qs = self._qs[offset : offset + limit]
        return (self._mapper(m) for m in sliced_qs)
