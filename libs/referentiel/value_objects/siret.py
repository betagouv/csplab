from pydantic import BaseModel, field_validator

SIRET_LENGTH = 14


class SIRET(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def validate_siret(cls, v: str) -> str:
        if not v.isdigit() or len(v) != SIRET_LENGTH:
            raise ValueError(f"Invalid SIRET: {v}")
        return v

    def __str__(self) -> str:
        return self.code
