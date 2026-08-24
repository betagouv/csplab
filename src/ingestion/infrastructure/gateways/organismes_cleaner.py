import csv
import logging
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, ValidationError, field_validator
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from domain.entities.raw_organisme import RawOrganisme

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_CATEGORIES_CSV = _DATA_DIR / "categories_entite_geographique_exercice.csv"

FINESS_REFERENTIEL = "FINESS"
GIPCDG_REFERENTIEL = "GIPCDG"


def _load_allowed_categories(csv_path: Path) -> set[str]:
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return {row["code"].strip() for row in reader if row.get("code")}


def _extract_coordinates(
    adresse: dict[str, Any],
) -> tuple[Optional[float], Optional[float]]:
    coordinates = adresse.get("coordonneesGeographique") or {}
    try:
        longitude = float(coordinates["coordonneeX"])
        latitude = float(coordinates["coordonneeY"])
    except (KeyError, TypeError, ValueError):
        return None, None
    return latitude, longitude


class Nom(BaseModel):
    value: str

    @field_validator("value")
    @classmethod
    def validate_nom(cls, v: str) -> str:
        nom = v.strip()
        if not nom:
            raise ValueError("nom is required")
        return nom


class FinessOrganismesCleaner:
    def __init__(self, categories_csv_path: Path = _CATEGORIES_CSV) -> None:
        self._allowed_categories = _load_allowed_categories(categories_csv_path)

    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        categorie = data.get("categorieentiteGeographiqueExercice")
        if categorie not in self._allowed_categories:
            return None

        infos = data.get("informationsGeneralesEGE") or {}
        nom = Nom(value=infos.get("nomEgeLong") or infos.get("nomEgeCourt") or "")

        localisation = None
        try:
            adresses = data.get("adresse") or []
            if adresses:
                adresse = adresses[0]
                cog_commune = adresse.get("cogCommune")
                department = (
                    Department.from_commune_code(cog_commune) if cog_commune else None
                )
                if department is not None:
                    latitude, longitude = _extract_coordinates(adresse)
                    localisation = Localisation.from_department(
                        department, latitude=latitude, longitude=longitude
                    )
        except ValidationError:
            logger.warning(
                "RawOrganisme %s has validation errors in localisation",
                raw_organisme.external_id,
            )

        return Organisme.build(
            entity_id=uuid4(),
            nom=nom.value,
            versant=Verse.FPH,
            siret=SIRET(code=infos.get("siret", "")),
            localisation=localisation,
            parent_id=None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
        )


class GipcdgOrganismesCleaner:
    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        nom = Nom(value=data.get("libl_col") or data.get("libc_col") or "")

        localisation = None
        cod_dep_col = data.get("cod_dep_col")
        if cod_dep_col:
            try:
                department = Department.from_department_code(cod_dep_col)
                if department is not None:
                    localisation = Localisation.from_department(department)
            except (ValidationError, ValueError):
                logger.warning(
                    "RawOrganisme %s has validation errors in localisation",
                    raw_organisme.external_id,
                )
        return Organisme.build(
            entity_id=uuid4(),
            nom=nom.value,
            versant=Verse.FPT,
            siret=SIRET(code=data.get("siret_col", "")),
            localisation=localisation,
            parent_id=None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
        )


class OrganismesCleaner:
    def __init__(self, categories_csv_path: Path = _CATEGORIES_CSV) -> None:
        self._finess_cleaner = FinessOrganismesCleaner(categories_csv_path)
        self._gipcdg_cleaner = GipcdgOrganismesCleaner()

    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if raw_organisme.referentiel == FINESS_REFERENTIEL:
            return self._finess_cleaner.clean(raw_organisme)
        if raw_organisme.referentiel == GIPCDG_REFERENTIEL:
            return self._gipcdg_cleaner.clean(raw_organisme)
        return None
