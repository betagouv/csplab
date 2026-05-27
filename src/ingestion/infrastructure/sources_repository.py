from domain.source import Source


class SourcesRepository:
    def __init__(self) -> None:
        self._mapping: dict[str, Source] = {}

    def load(self, sources: list[Source]) -> None:
        self._mapping = {s.client_id_back: s for s in sources}

    def get_by_client_id_back(self, client_id_back: str) -> Source | None:
        return self._mapping.get(client_id_back)

    def __len__(self) -> int:
        return len(self._mapping)
