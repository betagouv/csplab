from typing import ContextManager, Protocol


class IUnitOfWork(Protocol):
    # ContextManager check that atomic returns
    # a type compatible with "with" reserved keyword
    def atomic(self) -> ContextManager[None]: ...
