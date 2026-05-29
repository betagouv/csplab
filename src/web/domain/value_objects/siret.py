import re
from dataclasses import dataclass

from domain.exceptions.organisme_errors import InvalidSiretError


def luhn_checksum(value: str) -> bool:
    # Luhn algorithm for SIRET validation (same as SIREN)
    # https://calculio.fr/blog/valider-siren-siret-tva-intracommunautaire
    total = 0
    for i, digit in enumerate(reversed(value)):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:  # noqa
                n -= 9  # because input digits (0-9) can never exceed 18
        total += n
    return total % 10 == 0


@dataclass(frozen=True)
class SIRET:
    value: str

    def __post_init__(self):
        if not self.is_valid():
            raise InvalidSiretError(self.value)

    def is_valid(self) -> bool:
        if not re.match(r"^\d{14}$", self.value):
            return False
        return luhn_checksum(self.value)

    @property
    def siren(self) -> str:
        return self.value[:9]
