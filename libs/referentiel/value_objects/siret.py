from pydantic import BaseModel, ConfigDict, field_validator

SIRET_LENGTH = 14
LUHN_DIGIT_OVERFLOW_THRESHOLD = 9

# La Poste est historiquement exemptée de la validité de la clé de Luhn : son
# SIREN (356000000) a été attribué avant l'instauration de ce contrôle par
# l'INSEE, et ses SIRET ne la respectent pas.
LA_POSTE_SIREN = "356000000"


def _is_luhn_valid(digits: str) -> bool:
    total = 0
    for index, char in enumerate(reversed(digits)):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > LUHN_DIGIT_OVERFLOW_THRESHOLD:
                digit -= LUHN_DIGIT_OVERFLOW_THRESHOLD
        total += digit
    return total % 10 == 0


class SIRET(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str

    @field_validator("code")
    @classmethod
    def validate_siret(cls, v: str) -> str:
        if not v.isdigit() or len(v) != SIRET_LENGTH:
            raise ValueError(f"Invalid SIRET: {v}")
        if not v.startswith(LA_POSTE_SIREN) and not _is_luhn_valid(v):
            raise ValueError(f"Invalid SIRET checksum: {v}")
        return v

    def __str__(self) -> str:
        return self.code
