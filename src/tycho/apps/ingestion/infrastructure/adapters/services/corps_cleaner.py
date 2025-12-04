"""Corps cleaner adapter."""

from typing import List, Optional

import polars as pl

from apps.ingestion.infrastructure.adapters.services.pelage_checks import (
    has_no_minarm_ministry,
    has_only_civil_servants,
    has_only_fpe_type,
)
from core.entities.corps import Corps
from core.entities.document import Document, DocumentType
from core.errors.corps_errors import (
    InvalidAccessModalityError,
    InvalidDiplomaLevelError,
)
from core.errors.document_error import InvalidDocumentTypeError
from core.services.logger_interface import ILogger
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.diploma import Diploma
from core.value_objects.label import Label
from core.value_objects.ministry import Ministry

MAX_DECRETS_BY_CORPS = 20


class CorpsCleaner:
    """Adapter for cleaning raw documents of tye CORPS into Corps entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger.get_logger("CorpsCleaner::clean")

    def clean(self, raw_documents: List[Document]) -> List[Corps]:
        """Clean raw documents and return Corps entities using vectorized processing."""
        for document in raw_documents:
            if document.type != DocumentType.CORPS:
                raise InvalidDocumentTypeError(document.type.value)

        if not raw_documents:
            return []

        corps_data = []
        for document in raw_documents:
            parsed_data = self._parse_corps_data(document.raw_data)
            if parsed_data:
                corps_data.append(parsed_data)

        df = pl.DataFrame(corps_data)

        df_filtered = self._apply_filters(df)

        return self._dataframe_to_corps(df_filtered)

    def _parse_corps_data(self, raw_data: dict) -> Optional[dict]:
        """Parse raw corps data into structured format."""
        item = raw_data
        corps_libelle = item["corpsOuPseudoCorps"]["libelles"]["libelleLong"]

        sub_category = None
        if item["corpsOuPseudoCorps"]["sousCategorie"]:
            sub_category = item["corpsOuPseudoCorps"]["sousCategorie"][0][
                "libelleSousCategorie"
            ]

        category = None
        if sub_category:
            category = sub_category
        elif (
            item["corpsOuPseudoCorps"]["caracteristiques"]["categorie"][
                "libelleCategorie"
            ][-1]
            != "e"
        ):
            category = item["corpsOuPseudoCorps"]["caracteristiques"]["categorie"][
                "libelleCategorie"
            ][-1]

        diploma = None
        if item["corpsOuPseudoCorps"]["caracteristiques"]["niveauDiplome"]:
            diploma = item["corpsOuPseudoCorps"]["caracteristiques"]["niveauDiplome"][
                "libelleNiveauDiplome"
            ]

        access_mod = []
        if item["corpsOuPseudoCorps"]["dureeDeStageParModeAccesAuCorps"]:
            access_mod = [
                mod["modeAccesCorps"]["libelleModeAccesCorps"]
                for mod in item["corpsOuPseudoCorps"]["dureeDeStageParModeAccesAuCorps"]
            ]

        ministry = None
        if item["corpsOuPseudoCorps"]["ministereEtInstitutionDeLaRepublique"]:
            ministry = item["corpsOuPseudoCorps"][
                "ministereEtInstitutionDeLaRepublique"
            ][0]["libelleMinistere"]

        population = None
        if item["corpsOuPseudoCorps"]["caracteristiques"]["population"]:
            population = item["corpsOuPseudoCorps"]["caracteristiques"]["population"][
                "libellePopulation"
            ]

        law_ids = []
        law_desc = []
        law_nature = []
        if item["definitionsHistoriques"]["textesAssocies"]:
            law_ids = [
                text["numeroTexte"]
                for text in item["definitionsHistoriques"]["textesAssocies"]
            ]
            law_desc = [
                text["descriptif"]
                for text in item["definitionsHistoriques"]["textesAssocies"]
            ]
            law_nature = [
                text["nature"]["libelleNature"]
                for text in item["definitionsHistoriques"]["textesAssocies"]
                if text["nature"]
            ]

        return {
            "id": item["identifiant"],
            "category": category,
            "short_label": item["corpsOuPseudoCorps"]["libelles"]["libelleCourt"],
            "long_label": corps_libelle,
            "access_mod": access_mod,
            "diploma": diploma,
            "ministry": ministry,
            "fp_type": item["corpsOuPseudoCorps"]["caracteristiques"][
                "natureFonctionPublique"
            ]["libelleNatureFoncPub"],
            "population": population,
            "law_ids": law_ids,
            "law_desc": law_desc,
            "law_nature": law_nature,
        }

    def _apply_filters(self, df: pl.DataFrame) -> pl.DataFrame:
        """Apply filters: FPE only, no MINARM, fonctionnaire only."""
        df_filtered = df.filter(
            (pl.col("fp_type") == "FPE")
            & (pl.col("ministry") != "MINARM")
            & (pl.col("population") == "Fonctionnaire")
        )

        # Validate filtered data with pelage
        if len(df_filtered) > 0:
            df_filtered.pipe(has_only_fpe_type, "fp_type")
            df_filtered.pipe(has_no_minarm_ministry, "ministry")
            df_filtered.pipe(has_only_civil_servants, "population")

        return df_filtered.drop(["fp_type"])

    def _dataframe_to_corps(self, df: pl.DataFrame) -> List[Corps]:
        """Convert processed DataFrame back to Corps entities."""
        if len(df) == 0:
            return []

        corps_list = []
        for row in df.to_dicts():
            category = self._map_category(row["category"])
            ministry = self._map_ministry(row["ministry"])
            diploma = self._map_diploma(row["diploma"])
            access_modalities = self._map_access_modalities(row["access_mod"])

            corps = Corps(
                id=int(row["id"]),
                code=row["id"],  # Using id as code for now
                category=category,
                ministry=ministry,
                diploma=diploma,
                access_modalities=access_modalities,
                label=Label(
                    short_value=row["short_label"],
                    value=row["long_label"],
                ),
            )
            corps_list.append(corps)

        return corps_list

    def _map_category(self, category_str: Optional[str]) -> Optional[Category]:
        """Map category string to Category enum."""
        if not category_str:
            return None

        category_upper = category_str.upper()
        if "A+" in category_upper:
            return Category.APLUS
        elif "A" in category_upper:
            return Category.A
        elif "B" in category_upper:
            return Category.B
        else:
            return Category.C

    def _map_ministry(self, ministry_str: Optional[str]) -> Ministry:
        """Map ministry string to Ministry enum."""
        if ministry_str == "Météo France":
            return Ministry.METEO_FRANCE

        return Ministry(ministry_str)

    def _map_diploma(self, diploma_str: Optional[str]) -> Optional[Diploma]:
        """Map diploma string to Diploma value object using CNCP levels 1-8."""
        if not diploma_str:
            return None

        diploma_lower = diploma_str.lower()

        diploma_mappings = [
            (["niveau 8", "doctorat"], 8),
            (["niveau 7", "master"], 7),
            (["niveau 6", "licence"], 6),
            (["niveau 5", "bac + 2"], 5),
            (["niveau 4", "baccalauréat"], 4),
            (["niveau 3", "cap", "bep"], 3),
            (["niveau 2", "activités simples"], 2),
            (["niveau 1", "savoirs de base"], 1),
        ]

        for keywords, level in diploma_mappings:
            if any(keyword in diploma_lower for keyword in keywords):
                return Diploma(value=level)

        raise InvalidDiplomaLevelError(diploma_str)

    def _map_access_modalities(
        self, access_mod_list: List[str]
    ) -> List[AccessModality]:
        """Map access modality strings to AccessModality enums using direct mapping."""
        modalities = []
        for mod_str in access_mod_list:
            try:
                modality = AccessModality(mod_str)
                modalities.append(modality)
            except ValueError as err:
                raise InvalidAccessModalityError(mod_str) from err

        return modalities
