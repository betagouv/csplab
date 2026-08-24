import csv
import logging
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
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
DOM_TOM_DEPARTMENT_CODE_MIN = 971


def _load_allowed_categories(csv_path: Path) -> set[str]:
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return {row["code"].strip() for row in reader if row.get("code")}


def _external_id(info: ValidationInfo) -> str:
    if info.context is None:
        raise ValueError("Missing validation context")
    return str(info.context["external_id"])


class _ValidatedFields(BaseModel):
    nom: str
    siret: SIRET

    @field_validator("nom", mode="before")
    @classmethod
    def _clean_nom(cls, v: Optional[str], info: ValidationInfo) -> str:
        nom = v.strip() if v else ""
        if not nom:
            logger.warning("RawOrganisme %s has no nom, skipping", _external_id(info))
            raise ValueError("nom is required")
        return nom

    @field_validator("siret", mode="before")
    @classmethod
    def _build_siret(cls, v: Optional[str], info: ValidationInfo) -> SIRET:
        external_id = _external_id(info)
        if not v:
            logger.warning("RawOrganisme %s has no siret, skipping", external_id)
            raise ValueError("siret is required")
        try:
            return SIRET(code=v)
        except ValidationError:
            logger.warning("Invalid SIRET %s for organisme %s", v, external_id)
            raise


class OrganismesCleaner:
    def __init__(self, categories_csv_path: Path = _CATEGORIES_CSV) -> None:
        self._allowed_categories = _load_allowed_categories(categories_csv_path)

    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if raw_organisme.referentiel == FINESS_REFERENTIEL:
            return self._clean_finess(raw_organisme)
        if raw_organisme.referentiel == GIPCDG_REFERENTIEL:
            return self._clean_gipcdg(raw_organisme)
        return None

    def _clean_finess(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        categorie = data.get("categorieentiteGeographiqueExercice")
        if categorie not in self._allowed_categories:
            return None

        infos = data.get("informationsGeneralesEGE") or {}

        return self._build_organisme(
            raw_organisme,
            nom_raw=infos.get("nomEgeLong") or infos.get("nomEgeCourt"),
            siret_raw=infos.get("siret"),
            versant=Verse.FPH,
            localisation=self._map_localisation(data),
        )

    def _clean_gipcdg(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data

        return self._build_organisme(
            raw_organisme,
            nom_raw=data.get("libl_col") or data.get("libc_col"),
            siret_raw=data.get("siret_col"),
            versant=Verse.FPT,
            localisation=self._map_localisation_gipcdg(data),
        )

    def _build_organisme(
        self,
        raw_organisme: RawOrganisme,
        *,
        nom_raw: Optional[str],
        siret_raw: Optional[str],
        versant: Verse,
        localisation: Optional[Localisation],
    ) -> Optional[Organisme]:
        try:
            validated = _ValidatedFields.model_validate(
                {"nom": nom_raw, "siret": siret_raw},
                context={"external_id": raw_organisme.external_id},
            )
        except ValidationError:
            return None

        return Organisme.build(
            entity_id=uuid4(),
            nom=validated.nom,
            versant=versant,
            siret=validated.siret,
            localisation=localisation,
            parent_id=None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
        )

    def _map_localisation(self, data: dict[str, Any]) -> Optional[Localisation]:
        adresses = data.get("adresse") or []
        if not adresses:
            return None

        adresse = adresses[0]
        cog_commune = adresse.get("cogCommune")
        if not cog_commune:
            return None

        department = Department.from_commune_code(cog_commune)
        if department is None:
            return None

        latitude, longitude = self._extract_coordinates(adresse)

        return Localisation.from_department(
            department, latitude=latitude, longitude=longitude
        )

    def _map_localisation_gipcdg(self, data: dict[str, Any]) -> Optional[Localisation]:
        cod_dep_col = data.get("cod_dep_col")
        if not cod_dep_col:
            return None

        department = self._department_from_cod_dep(cod_dep_col)
        if department is None:
            return None

        return Localisation.from_department(department)

    def _department_from_cod_dep(self, cod_dep_col: str) -> Optional[Department]:
        stripped = cod_dep_col.strip().lstrip("0")
        if not stripped:
            return None
        try:
            numero = int(stripped)
        except ValueError:
            return None
        code = (
            f"{numero:03d}"
            if numero >= DOM_TOM_DEPARTMENT_CODE_MIN
            else f"{numero:02d}"
        )
        try:
            return Department(code=code)
        except ValidationError:
            return None

    def _extract_coordinates(
        self, adresse: dict[str, Any]
    ) -> tuple[Optional[float], Optional[float]]:
        coordinates = adresse.get("coordonneesGeographique") or {}
        try:
            longitude = float(coordinates["coordonneeX"])
            latitude = float(coordinates["coordonneeY"])
        except (KeyError, TypeError, ValueError):
            return None, None
        return latitude, longitude
