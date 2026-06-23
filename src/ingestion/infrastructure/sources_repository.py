from referentiel.entities.source import Source


class SourcesRepository:
    def __init__(self) -> None:
        self._mapping: dict[str, Source] = {}

    def load(self, sources: list[Source]) -> None:
        self._mapping = {s.client_id_back: s for s in sources}

    def get_by_client_id_back(self, client_id_back: str) -> Source | None:
        return self._mapping.get(client_id_back)

    def get_by_source_id(self, source_id: str) -> Source | None:
        return next(
            (s for s in self._mapping.values() if s.source_id == source_id), None
        )

    def __len__(self) -> int:
        return len(self._mapping)
