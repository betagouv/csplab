class MetiersMultiDomainesRepository:
    def __init__(self) -> None:
        self._codes: frozenset[str] = frozenset()

    def load(self, codes: set[str]) -> None:
        self._codes = frozenset(codes)

    def __contains__(self, code: object) -> bool:
        return code in self._codes
