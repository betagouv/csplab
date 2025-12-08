"""Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

MIN_NOR_LENGTH = 10


class ConcoursRowSchema(BaseModel):
    """Schema for validating a single concours row from CSV."""

    nor: str = Field(..., alias="N° NOR", min_length=1)
    nor_reference: Optional[str] = Field(None, alias="N° NOR de référence")
    ministere: str = Field(..., alias="Ministère", min_length=1)
    ministere_initial: Optional[str] = Field(None, alias="Ministère (saisie initiale)")
    categorie: str = Field(..., alias="Catégorie", min_length=1)
    corps: str = Field(..., alias="Corps", min_length=1)
    grade: str = Field(..., alias="Grade", min_length=1)
    corps_grade_initial: Optional[str] = Field(
        None, alias="Corps/Grade (saisie initiale)"
    )
    direction_etablissement: Optional[str] = Field(
        None, alias="Direction/Établissement"
    )
    annee_reference: int = Field(..., alias="Année de référence", ge=2015, le=2030)
    statut: Optional[str] = Field(None, alias="Statut")
    date_premiere_epreuve: Optional[str] = Field(None, alias="Date de première épreuve")

    # Modalités d'accès (colonnes booléennes)
    national: Optional[bool] = Field(None, alias="National")
    national_affectation_locale: Optional[bool] = Field(
        None, alias="National à affectation locale"
    )
    deconcentre: Optional[bool] = Field(None, alias="Déconcentré")
    externe: Optional[int] = Field(None, alias="Externe", ge=0)
    interne: Optional[int] = Field(None, alias="Interne", ge=0)
    troisieme_concours: Optional[int] = Field(None, alias="Troisieme Concours", ge=0)
    unique: Optional[int] = Field(None, alias="Unique", ge=0)
    examen_professionnel: Optional[int] = Field(
        None, alias="Examen professionnel", ge=0
    )
    sans_concours_externe: Optional[int] = Field(
        None, alias="Sans concours externe", ge=0
    )
    pacte: Optional[int] = Field(None, alias="Pacte", ge=0)
    selection_professionnelle: Optional[int] = Field(
        None, alias="Sélection professionnelle", ge=0
    )
    concours_special: Optional[int] = Field(None, alias="Concours spécial", ge=0)
    concours_reserve: Optional[int] = Field(None, alias="Concours réservé", ge=0)
    sans_concours_interne_reserve: Optional[int] = Field(
        None, alias="Sans concours interne réservé", ge=0
    )
    examen_professionnalise_reserve: Optional[int] = Field(
        None, alias="Examen professionnalisé réservé", ge=0
    )
    interne_exceptionnel: Optional[int] = Field(
        None, alias="Interne exceptionnel", ge=0
    )
    apprenti_boeth: Optional[int] = Field(None, alias="Apprenti BOETH", ge=0)
    promotion_boeth: Optional[int] = Field(None, alias="Promotion BOETH", ge=0)
    autres: Optional[int] = Field(None, alias="Autres", ge=0)

    # Nombre de postes
    nb_postes_acvg: Optional[int] = Field(None, alias="Nb postes ACVG", ge=0)
    nb_postes_th: Optional[int] = Field(None, alias="Nb postes TH", ge=0)
    nb_postes_total: int = Field(..., alias="Nb postes total", ge=0)

    @validator("date_premiere_epreuve")
    def validate_date_format(cls, v):
        """Validate date format DD/MM/YYYY."""
        if v is None or v == "":
            return None
        try:
            datetime.strptime(v, "%d/%m/%Y")
            return v
        except ValueError as err:
            raise ValueError("Date must be in DD/MM/YYYY format") from err

    @validator("nor")
    def validate_nor_format(cls, v):
        """Basic NOR format validation."""
        if not v or len(v) < MIN_NOR_LENGTH:
            raise ValueError(f"NOR must be at least {MIN_NOR_LENGTH} characters long")
        return v.upper()

    @validator(
        "national",
        "national_affectation_locale",
        "deconcentre",
        pre=True,
    )
    def parse_french_boolean(cls, v):
        """Parse French boolean values (Oui/Non) to Python boolean."""
        if isinstance(v, str):
            v_lower = v.strip().lower()
            if v_lower in ["oui", "o", "1", "true", "vrai"]:
                return True
            elif v_lower in ["non", "n", "0", "false", "faux"]:
                return False
            elif v_lower == "":
                return None
        return v

    class Config:
        """Pydantic config."""

        validate_by_name = True
        str_strip_whitespace = True


class ConcoursUploadResponse(BaseModel):
    """Response schema for concours upload."""

    status: str
    message: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    created: int
    updated: int
    errors: Optional[list] = None
