from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    client_id: str
    client_secret: str
    base_url: str
