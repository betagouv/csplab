from typing import List, Protocol

from referentiel.entities.source import Source


class ISourceRepository(Protocol):
    def get_all(self) -> List[Source]: ...
