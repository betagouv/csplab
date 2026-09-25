from dataclasses import dataclass
from typing import Optional


@dataclass
class TalentsoftOrganisme:
    entity_code: str
    code: int
    name: str
    parent_code: Optional[int] = None
    has_children: bool = False
    description: Optional[str] = None
    url: Optional[str] = None
    phone_number: Optional[str] = None
    post_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    parent_name: Optional[str] = None
    logo_url: Optional[str] = None
    max_delay_for_consent: Optional[int] = None
    retention_period: Optional[int] = None
    general_conditions: Optional[str] = None
    personal_data_consent: Optional[str] = None
