from datetime import datetime
from typing import Optional

from drf_spectacular.utils import OpenApiExample
from pydantic import BaseModel, ConfigDict, Field, field_validator

MIN_NOR_LENGTH = 10


class ConcoursRowSchema(BaseModel):
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


list_offers_view_description = """
# API de consultation des offres d'emploi de la Fonction Publique

Cette API retourne la liste de offres correspondant à une recherche selon les 3
critères suivants :

- Candidature active / archivée
- Mise à jour avant une date-heure
- Mise à jour après une date-heure

Cette API est à l’usage exclusif des personnes autorisées.

# Permissions

L’utilisation de cette API nécessite un token d’autorisation spécifique à chaque
utilisateur.

# Limitations

L’interrogation de cette API est limitée à 120 appels par minute et par utilisateur.
"""

list_offers_response_valid_example = OpenApiExample(
    "Exemple de liste d'offres d'emploi (réponse)",
    response_only=True,
    status_codes=[200],
    value={
        "external_id": "Versant_FPE-2026-999999",
        "title": "Responsable de la Division des Affaires Financières H/F",
        "organization": "Ecole Nationale Supérieure de Techniques Avancées (ENSTA)",
        "contract_type": "TITULAIRE_CONTRACTUEL",
        "category": "A",
        "publication_date": "2026-04-17T14:44:49.873000+00:00",
        "offer_url": "https://test.com/offre-emploi/2026-999999/",
    },
)
