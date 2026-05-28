class CredentialsStore:
    def __init__(self) -> None:
        self._mapping: dict[str, str] = {}

    def register(self, client_id: str, secret: str) -> None:
        self._mapping[client_id] = secret

    def get_secret(self, client_id: str) -> str | None:
        return self._mapping.get(client_id)

    def __len__(self) -> int:
        return len(self._mapping)
