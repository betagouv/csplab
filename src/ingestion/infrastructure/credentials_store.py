from domain.value_objects.credentials import Credentials


class CredentialsStore:
    def __init__(self) -> None:
        self._credentials: dict[str, Credentials] = {}

    def register(self, credentials: Credentials) -> None:
        self._credentials[credentials.client_id] = credentials

    def get_secret(self, client_id: str) -> str | None:
        creds = self._credentials.get(client_id)
        return creds.client_secret if creds else None

    def get_credentials(self, client_id: str) -> Credentials | None:
        return self._credentials.get(client_id)

    def __len__(self) -> int:
        return len(self._credentials)
