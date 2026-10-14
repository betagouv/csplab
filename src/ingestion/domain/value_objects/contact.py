from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional

from domain.value_objects.email import extract_emails


class ContactRole(StrEnum):
    PRINCIPAL = "principal"
    AUTRE = "autre"


@dataclass(frozen=True)
class Contact:
    role: ContactRole
    text: str
    emails: list[str] = field(default_factory=list)

    @classmethod
    def from_text(cls, role: ContactRole, text: Optional[str]) -> Optional["Contact"]:
        stripped = (text or "").strip()
        if not any(char.isalnum() for char in stripped):
            return None
        return cls(role=role, text=stripped, emails=extract_emails(stripped))
