import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4, uuid5

from pydantic import BaseModel, ValidationError, field_validator
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from domain.entities.raw_organisme import RawOrganisme
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.gateways.lambert93 import lambert93_to_wgs84

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
# From https://smt.esante.gouv.fr/fhir/CodeSystem/tre-r397-categorie-entite-geographique-exercice
_CATEGORIES_CSV = _DATA_DIR / "categories_entite_geographique_exercice.csv"

_MAX_LONGITUDE_DEGREES = 180
_MAX_LATITUDE_DEGREES = 90

# Namespace utilisé pour dériver un entity_id stable à partir de l'external_id
# DILA, afin que le parent_id reconstruit à l'import référence le même UUID
# que celui utilisé pour construire l'organisme parent.
_DILA_NAMESPACE = uuid5(UUID(int=0), "csplab.ingestion.dila.organisme")


def _dila_entity_id(external_id: str) -> UUID:
    return uuid5(_DILA_NAMESPACE, external_id)


def _parse_date(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%d/%m/%Y").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _parse_iso_date(value: Any) -> Optional[date]:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _load_allowed_categories(csv_path: Path) -> set[str]:
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return {row["code"].strip() for row in reader if row.get("code")}


class Nom(BaseModel):
    value: str

    @field_validator("value")
    @classmethod
    def validate_nom(cls, v: str) -> str:
        nom = v.strip()
        if not nom:
            raise ValueError("nom is required")
        return nom


class OrganismesCleaner:
    def __init__(self, categories_csv_path: Path = _CATEGORIES_CSV) -> None:
        self._allowed_categories = _load_allowed_categories(categories_csv_path)

    def clean(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if raw_organisme.referentiel == OrganismeReferentiel.FINESS:
            return self._clean_finess(raw_organisme)
        if raw_organisme.referentiel == OrganismeReferentiel.GIPCDG:
            return self._clean_gipcdg(raw_organisme)
        if raw_organisme.referentiel == OrganismeReferentiel.DILA:
            return self._clean_dila(raw_organisme)
        return None

    def dedupe_by_siret(self, organismes: list[Organisme]) -> list[Organisme]:
        best_by_siret: dict[SIRET, Organisme] = {}
        for organisme in organismes:
            current_best = best_by_siret.get(organisme.siret)
            if current_best is None or self._is_better(organisme, current_best):
                best_by_siret[organisme.siret] = organisme
        return list(best_by_siret.values())

    @classmethod
    def _is_better(cls, candidate: Organisme, current_best: Organisme) -> bool:
        # Le plus récemment créé l'emporte ; à égalité (ou en l'absence de
        # date_creation, ex. FINESS), le plus petit external_id l'emporte.
        candidate_date = candidate.date_creation
        best_date = current_best.date_creation
        if candidate_date != best_date:
            if best_date is None:
                return True
            if candidate_date is None:
                return False
            return candidate_date > best_date
        return cls._external_id_key(candidate) < cls._external_id_key(current_best)

    @staticmethod
    def _is_active_porteuse(data: dict[str, Any], infos: dict[str, Any]) -> bool:
        if data.get("etatObjet") != "A":
            return False
        ege_id = infos.get("egeId")
        roles_ege = data.get("roleEge") or []
        return any(role.get("idEgePorteuse") == ege_id for role in roles_ege)

    @staticmethod
    def _external_id_key(organisme: Organisme) -> tuple[int, int | str]:
        external_id = organisme.external_id or ""
        try:
            return (0, int(external_id))
        except ValueError:
            return (1, external_id)

    def _clean_finess(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        infos = data.get("informationsGeneralesEGE") or {}
        if not self._is_active_porteuse(data, infos):
            return None

        categorie = data.get("categorieentiteGeographiqueExercice")
        if categorie not in self._allowed_categories:
            return None

        nom = Nom(value=infos.get("nomEgeLong") or infos.get("nomEgeCourt") or "")
        siret = SIRET(code=infos.get("siret", ""))
        localisation = self._map_localisation(data, raw_organisme.external_id)

        return Organisme.build(
            entity_id=uuid4(),
            nom=nom.value,
            versant=Verse.FPH,
            siret=siret,
            localisation=localisation,
            parent_id=None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
        )

    def _clean_gipcdg(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        if data.get("is_attached"):
            # Secteurs internes rattachés à une collectivité mère (même SIRET)
            # via col_mere_id : ce ne sont pas des organismes distincts.
            return None

        nom = Nom(value=data.get("libl_col") or data.get("libc_col") or "")
        siret = SIRET(code=data.get("siret_col", ""))
        localisation = self._map_localisation_gipcdg(data, raw_organisme.external_id)

        return Organisme.build(
            entity_id=uuid4(),
            nom=nom.value,
            versant=Verse.FPT,
            siret=siret,
            localisation=localisation,
            parent_id=None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
            date_creation=_parse_date(data.get("date_insert_col")),
        )

    def _clean_dila(self, raw_organisme: RawOrganisme) -> Optional[Organisme]:
        if not raw_organisme.data:
            return None

        data = raw_organisme.data
        nom = Nom(value=data.get("nom") or "")
        siret = SIRET(code=data.get("siret") or "")
        localisation = self._map_localisation_dila(data, raw_organisme.external_id)

        parent_external_id = data.get("parent_id") or None

        return Organisme.build(
            entity_id=_dila_entity_id(raw_organisme.external_id),
            nom=nom.value,
            versant=Verse.FPE,
            siret=siret,
            localisation=localisation,
            parent_id=_dila_entity_id(parent_external_id)
            if parent_external_id
            else None,
            external_id=raw_organisme.external_id,
            referentiel=raw_organisme.referentiel,
            millesime=raw_organisme.millesime,
            date_creation=_parse_iso_date(data.get("date_creation_datetime")),
        )

    def _map_localisation_dila(
        self, data: dict[str, Any], external_id: str
    ) -> Optional[Localisation]:
        localisation = None
        code_insee_commune = data.get("code_insee_commune")
        if code_insee_commune:
            try:
                department = Department.from_commune_code(code_insee_commune)
                latitude, longitude = self._extract_coordinates_dila(data)
                localisation = Localisation.from_department(
                    department, latitude=latitude, longitude=longitude
                )
            except (ValidationError, ValueError):
                logger.warning(
                    "RawOrganisme %s has validation errors in localisation",
                    external_id,
                )
        return localisation

    @staticmethod
    def _extract_coordinates_dila(
        data: dict[str, Any],
    ) -> tuple[Optional[float], Optional[float]]:
        try:
            adresses = json.loads(data.get("adresse") or "[]")
        except (TypeError, ValueError):
            return None, None

        for adresse in adresses:
            try:
                longitude = float(adresse.get("longitude"))
                latitude = float(adresse.get("latitude"))
            except (TypeError, ValueError):
                continue
            return latitude, longitude
        return None, None

    def _map_localisation(
        self, data: dict[str, Any], external_id: str
    ) -> Optional[Localisation]:
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
                    latitude, longitude = self._extract_coordinates(adresse)
                    localisation = Localisation.from_department(
                        department, latitude=latitude, longitude=longitude
                    )
        except (ValidationError, ValueError):
            logger.warning(
                "RawOrganisme %s has validation errors in localisation", external_id
            )
        return localisation

    def _map_localisation_gipcdg(
        self, data: dict[str, Any], external_id: str
    ) -> Optional[Localisation]:
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
                    external_id,
                )
        return localisation

    def _extract_coordinates(
        self, adresse: dict[str, Any]
    ) -> tuple[Optional[float], Optional[float]]:
        coordinates = adresse.get("coordonneesGeographique") or {}
        try:
            x = float(coordinates["coordonneeX"])
            y = float(coordinates["coordonneeY"])
        except (KeyError, TypeError, ValueError):
            return None, None

        # FINESS sometimes publishes coordinates projected in Lambert-93
        # (meters) instead of WGS84 decimal degrees.
        if abs(x) > _MAX_LONGITUDE_DEGREES or abs(y) > _MAX_LATITUDE_DEGREES:
            return lambert93_to_wgs84(x, y)

        return y, x
