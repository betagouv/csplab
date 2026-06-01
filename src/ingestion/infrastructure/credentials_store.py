from domain.value_objects.credentials import Credentials


class CredentialsStore:
    def __init__(self) -> None:
        self._credentials: dict[str, Credentials] = {}

    def register(self, client_id: str, client_secret: str, base_url: str) -> None:
        self._credentials[client_id] = Credentials(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
        )

    def get_secret(self, client_id: str) -> str | None:
        creds = self._credentials.get(client_id)
        return creds.client_secret if creds else None

    def get_credentials(self, client_id: str) -> Credentials | None:
        return self._credentials.get(client_id)

    def __len__(self) -> int:
        return len(self._credentials)
