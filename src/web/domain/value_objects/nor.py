import re
from dataclasses import dataclass

from domain.exceptions.concours_errors import InvalidNorError


@dataclass(frozen=True)
class NOR:
    value: str

    def __post_init__(self):
        if not self.is_valid():
            raise InvalidNorError(f"Invalid NOR format: {self.value}")

    def is_valid(self) -> bool:
        pattern = r"^[A-Z]{4}\d{7}[A-Z]$"
        return bool(re.match(pattern, self.value))

    def extract_year(self) -> int:
        return int(self.value[4:6]) + 2000  # Assuming 20XX format

    def extract_sequence(self) -> int:
        return int(self.value[6:11])
