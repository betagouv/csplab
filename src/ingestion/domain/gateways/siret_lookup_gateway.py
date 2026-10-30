from typing import Protocol

from domain.value_objects.siret_candidate import SiretCandidate


class ISiretLookupGateway(Protocol):
    def search(self, query: str) -> list[SiretCandidate]:
        """Candidates matching a name or a SIRET.

        Raises an exception when the lookup itself fails, so that a failed
        call is not mistaken for an empty result and cached as such.
        """
        ...
