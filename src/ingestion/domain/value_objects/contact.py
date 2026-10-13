import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional

# Conservative pattern: an extracted address must pass the web API's EmailField
# validation, otherwise the whole offer is rejected.
_EMAIL_PATTERN = re.compile(
    r"(?<![\w.%+-])"
    r"[A-Za-z0-9_%+-]+(?:\.[A-Za-z0-9_%+-]+)*"
    r"@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
    r"(?!\w)"
)


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
        emails = list(dict.fromkeys(_EMAIL_PATTERN.findall(stripped)))
        return cls(role=role, text=stripped, emails=emails)
