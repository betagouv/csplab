from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    source_id: str
    type: str
    client_id_front: str
    client_id_back: str
    base_url_front: str
    base_url_back: str
