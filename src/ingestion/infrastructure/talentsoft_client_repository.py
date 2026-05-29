from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient


class TalentsoftClientRepository:
    def __init__(self) -> None:
        self._clients: dict[str, TalentsoftFrontClient] = {}

    def register(self, client_id: str, client: TalentsoftFrontClient) -> None:
        self._clients[client_id] = client

    def get(self, client_id: str) -> TalentsoftFrontClient | None:
        return self._clients.get(client_id)
