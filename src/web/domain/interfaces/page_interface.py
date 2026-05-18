from typing import Iterator, Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class IPage(Protocol[T_co]):
    def count(self) -> int: ...
    def slice(self, offset: int, limit: int) -> Iterator[T_co]: ...
