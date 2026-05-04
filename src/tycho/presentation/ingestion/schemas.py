from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

MIN_NOR_LENGTH = 10


class ConcoursRowSchema(BaseModel):
    nor: str = Field(..., min_length=1)
    nor_reference: Optional[str] = Field(None)
    ministere: str = Field(..., min_length=1)
    ministere_initial: Optional[str] = Field(None)
    categorie: str = Field(..., min_length=1)
    corps: str = Field(..., min_length=1)
    grade: str = Field(..., min_length=1)
    corps_grade_initial: Optional[str] = Field(None)
    direction_etablissement: Optional[str] = Field(None)
    annee_reference: int = Field(..., ge=2015, le=2030)
    statut: Optional[str] = Field(None)
    date_premiere_epreuve: Optional[str] = Field(None)

    # Modalités d'accès (colonnes booléennes)
    national: Optional[bool] = Field(None)
    national_affectation_locale: Optional[bool] = Field(None)
    deconcentre: Optional[bool] = Field(None)
    externe: Optional[int] = Field(None, ge=0)
    interne: Optional[int] = Field(None, ge=0)
    troisieme_concours: Optional[int] = Field(None, ge=0)
    unique: Optional[int] = Field(None, ge=0)
    examen_professionnel: Optional[int] = Field(None, ge=0)
    sans_concours_externe: Optional[int] = Field(None, ge=0)
    pacte: Optional[int] = Field(None, ge=0)
    selection_professionnelle: Optional[int] = Field(None, ge=0)
    concours_special: Optional[int] = Field(None, ge=0)
    concours_reserve: Optional[int] = Field(None, ge=0)
    sans_concours_interne_reserve: Optional[int] = Field(None, ge=0)
    examen_professionnalise_reserve: Optional[int] = Field(None, ge=0)
    interne_exceptionnel: Optional[int] = Field(None, ge=0)
    apprenti_boeth: Optional[int] = Field(None, ge=0)
    promotion_boeth: Optional[int] = Field(None, ge=0)
    autres: Optional[int] = Field(None, ge=0)

    # Nombre de postes
    nb_postes_acvg: Optional[int] = Field(None, ge=0)
    nb_postes_th: Optional[int] = Field(None, ge=0)
    nb_postes_total: int = Field(..., ge=0)

    @field_validator("date_premiere_epreuve")
    @classmethod
    def validate_date_format(cls, v):
        if v is None or v == "":
            return None
        try:
            datetime.strptime(v, "%d/%m/%Y")
            return v
        except ValueError as err:
            raise ValueError("Date must be in DD/MM/YYYY format") from err

    @field_validator("nor")
    @classmethod
    def validate_nor_format(cls, v):
        if not v or len(v) < MIN_NOR_LENGTH:
            raise ValueError(f"NOR must be at least {MIN_NOR_LENGTH} characters long")
        return v.upper()

    @field_validator(
        "national",
        "national_affectation_locale",
        "deconcentre",
        mode="before",
    )
    @classmethod
    def parse_french_boolean(cls, v):
        if isinstance(v, str):
            v_lower = v.strip().lower()
            if v_lower in ["oui", "o", "1", "true", "vrai"]:
                return True
            elif v_lower in ["non", "n", "0", "false", "faux"]:
                return False
            elif v_lower == "":
                return None
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class ConcoursUploadResponse(BaseModel):
    status: str
    message: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    created: int
    updated: int
    errors: Optional[list] = None
