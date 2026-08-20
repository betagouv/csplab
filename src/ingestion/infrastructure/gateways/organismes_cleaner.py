import csv
import logging
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from pydantic import ValidationError
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


def _load_allowed_categories(csv_path: Path) -> set[str]:
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return {row["code"].strip() for row in reader if row.get("code")}


class OrganismesCleaner:
    def __init__(self, categories_csv_path: Path = _CATEGORIES_CSV) -> None:
        self._allowed_categories = _load_allowed_categories(categories_csv_path)

    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if raw_organisme.referentiel != FINESS_REFERENTIEL:
            return None
        return self._clean_finess(raw_organisme)

    def _clean_finess(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        categorie = data.get("categorieentiteGeographiqueExercice")
        if categorie not in self._allowed_categories:
            return None

        infos = data.get("informationsGeneralesEGE") or {}

        nom = self._map_nom(infos)
        if not nom:
            logger.warning(
                "RawOrganisme %s has no nom, skipping", raw_organisme.external_id
            )
            return None

        siret = self._map_siret(infos, raw_organisme.external_id)
        if siret is None:
            return None

        localisation = self._map_localisation(data)

        return Organisme.build(
            entity_id=uuid4(),
            nom=nom,
            versant=Verse.FPH,
            siret=siret,
            localisation=localisation,
            parent_id=None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
        )

    def _map_nom(self, infos: dict[str, Any]) -> Optional[str]:
        nom = infos.get("nomEgeLong") or infos.get("nomEgeCourt")
        return nom.strip() if nom else None

    def _map_siret(self, infos: dict[str, Any], external_id: str) -> Optional[SIRET]:
        siret_str = infos.get("siret")
        if not siret_str:
            logger.warning("RawOrganisme %s has no siret, skipping", external_id)
            return None
        try:
            return SIRET(code=siret_str)
        except ValidationError:
            logger.warning("Invalid SIRET %s for organisme %s", siret_str, external_id)
            return None

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
