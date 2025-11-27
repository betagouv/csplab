"""Corps cleaner adapter."""

import re
from typing import List, Optional

import polars as pl

from core.entities.corps import Corps
from core.entities.document import Document, DocumentType
from core.errors.domain_errors import InvalidDocumentTypeError
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

        if not corps_data:
            return []

        df = pl.DataFrame(corps_data)

        # Apply filters (FPE, no MINARM, fonctionnaire)
        df_filtered = self._apply_filters(df)

        # Process laws and select best decree
        df_processed = self._process_laws(df_filtered)

        # Convert back to Corps entities
        return self._dataframe_to_corps(df_processed)

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
        return df.filter(
            (pl.col("fp_type") == "FPE")
            & (pl.col("ministry") != "MINARM")
            & (pl.col("population") == "Fonctionnaire")
        ).drop(["fp_type"])

    def _process_laws(self, df: pl.DataFrame) -> pl.DataFrame:
        """Process laws and select best decree for each corps."""
        # Explode laws to have one row per law
        df_expanded = (
            df.explode(["law_ids", "law_desc", "law_nature"])
            .rename(
                {
                    "law_ids": "law_id",
                    "law_desc": "law_desc",
                    "law_nature": "law_nature",
                }
            )
            .filter(pl.col("law_id").is_not_null())
        )

        # Calculate law frequencies
        law_freq = df_expanded.group_by("law_id").len().rename({"len": "count"})

        # Join frequencies back
        df_with_freq = df_expanded.join(law_freq, on="law_id", how="left")

        # Group by corps and select best law
        results = []
        for corps_id in df_with_freq["id"].unique():
            corps_laws = df_with_freq.filter(pl.col("id") == corps_id)
            base_info = corps_laws.row(0, named=True)

            # Convert to list of dicts for law selection
            laws_list = corps_laws.to_dicts()
            selected_law = self._select_best_law(laws_list)

            if selected_law:
                result = {
                    "id": corps_id,
                    "category": base_info["category"],
                    "short_label": base_info["short_label"],
                    "long_label": base_info["long_label"],
                    "access_mod": base_info["access_mod"],
                    "diploma": base_info["diploma"],
                    "ministry": base_info["ministry"],
                    "selected_law_id": selected_law["law_id"],
                    "selected_law_desc": selected_law["law_desc"],
                    "selected_law_nature": selected_law["law_nature"],
                }
                results.append(result)

        return pl.DataFrame(results) if results else pl.DataFrame()

    def _has_valid_decree_format(self, law_id: str) -> bool:
        """Check if law_id has valid decree format (YYYY-NNNN or YY-NNNN)."""
        if not law_id:
            return False
        pattern = r"^\d{2,4}-\d+$"
        return bool(re.match(pattern, str(law_id)))

    def _select_best_law(self, laws_list: List[dict]) -> Optional[dict]:
        """Select best law from list - prioritize valid decree format."""
        # Rule 1: filter out too generic laws (referenced in more than 20 bodies)
        candidates = [law for law in laws_list if law["count"] <= MAX_DECRETS_BY_CORPS]

        if not candidates:
            return None

        # Rule 2: valid decree format (regardless of nature)
        valid_decree_laws = [
            law for law in candidates if self._has_valid_decree_format(law["law_id"])
        ]

        if not valid_decree_laws:
            return None

        # Rule 3: prefer origin texts, the most specific one (least frequent)
        origin_valid = [
            law for law in valid_decree_laws if law["law_nature"] == "Texte d'origine"
        ]
        if origin_valid:
            return min(origin_valid, key=lambda x: x["count"])

        # Rule 4: otherwise, modificative texts, the most specific one (least frequent)
        modif_valid = [
            law for law in valid_decree_laws if law["law_nature"] == "Texte modificatif"
        ]
        if modif_valid:
            return min(modif_valid, key=lambda x: x["count"])

        # Rule 5: fallback on least frequent
        return min(candidates, key=lambda x: x["count"])

    def _dataframe_to_corps(self, df: pl.DataFrame) -> List[Corps]:
        """Convert processed DataFrame back to Corps entities."""
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

    def _map_category(self, category_str: Optional[str]) -> Category:
        """Map category string to Category enum."""
        if not category_str:
            return Category.A  # Default

        category_upper = category_str.upper()
        if "A" in category_upper:
            return Category.A
        elif "B" in category_upper:
            return Category.B
        elif "C" in category_upper:
            return Category.C
        else:
            return Category.A  # Default

    def _map_ministry(self, ministry_str: Optional[str]) -> Ministry:
        """Map ministry string to Ministry enum."""
        if not ministry_str:
            return Ministry.MEN  # Default

        # Simple mapping - can be extended
        ministry_upper = ministry_str.upper()
        if "EDUCATION" in ministry_upper or "MEN" in ministry_upper:
            return Ministry.MEN
        else:
            return Ministry.MEN  # Default for now

    def _map_diploma(self, diploma_str: Optional[str]) -> Optional[Diploma]:
        """Map diploma string to Diploma value object."""
        if not diploma_str:
            return None

        # Extract numeric level from diploma string
        if "BAC+5" in diploma_str.upper() or "MASTER" in diploma_str.upper():
            return Diploma(value=5)
        elif "BAC+3" in diploma_str.upper() or "LICENCE" in diploma_str.upper():
            return Diploma(value=3)
        elif "BAC" in diploma_str.upper():
            return Diploma(value=0)
        else:
            return Diploma(value=4)  # Default

    def _map_access_modalities(
        self, access_mod_list: List[str]
    ) -> List[AccessModality]:
        """Map access modality strings to AccessModality enums."""
        if not access_mod_list:
            return [AccessModality.CONCOURS_EXTERNE]  # Default

        modalities = []
        for mod_str in access_mod_list:
            mod_upper = mod_str.upper()
            if "EXTERNE" in mod_upper:
                modalities.append(AccessModality.CONCOURS_EXTERNE)
            elif "INTERNE" in mod_upper:
                modalities.append(AccessModality.CONCOURS_INTERNE)
            # Add more mappings as needed

        return modalities if modalities else [AccessModality.CONCOURS_EXTERNE]
