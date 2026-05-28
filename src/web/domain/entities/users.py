from dataclasses import dataclass

from pydantic import EmailStr

from domain.interfaces.entity_interface import IEntity


@dataclass
class User(IEntity):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
