"""Corps cleaner adapter."""

from typing import List, Optional

import polars as pl

from apps.ingestion.infrastructure.adapters.services.pelage_checks import (
    has_no_minarm_ministry,
    has_only_civil_servants,
    has_only_fpe_type,
)
from core.entities.concours import Concours
from core.entities.document import Document, DocumentType
from core.errors.corps_errors import InvalidAccessModalityError, InvalidCategoryError
from core.errors.document_error import InvalidDocumentTypeError
from core.services.document_cleaner_interface import IDocumentCleaner
from core.services.logger_interface import ILogger
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry


class ConcoursCleaner(IDocumentCleaner[Concours]):
    """Adapter for cleaning raw documents of type CONCOURS into Concours entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger.get_logger("ConcoursCleaner::clean")

    def clean(self, raw_documents: List[Document]) -> List[Concours]:
        """Clean raw documents and return Concours entities."""
        for document in raw_documents:
            if document.type != DocumentType.CONCOURS:
                raise InvalidDocumentTypeError(document.type.value)

        concours_data = []
        for document in raw_documents:
            parsed_data = self._parse_concours_data(document.raw_data)
            if parsed_data:
                concours_data.append(parsed_data)

        df = pl.DataFrame(concours_data)

        df_filtered = self._apply_filters(df)

        return self._dataframe_to_concours(df_filtered)

    def _parse_concours_data(self, raw_data: dict) -> Optional[dict]:
        """Parse raw concours data into structured format."""
        return {}

    def _apply_filters(self, df: pl.DataFrame) -> pl.DataFrame:
        """Apply filters: no MINARM, current concours only."""
        df_filtered = df.filter(
            (pl.col("Ministère") == "Ministère des Armées")
            & (pl.col("Corps") != "")
            & (pl.col("Grade") != "")
            & (pl.col("Catégorie") != "")
        )

        # Validate filtered data with pelage
        if len(df_filtered) > 0:
            df_filtered.pipe(has_only_fpe_type, "fp_type")
            df_filtered.pipe(has_no_minarm_ministry, "ministry")
            df_filtered.pipe(has_only_civil_servants, "population")

        return df_filtered.drop(["fp_type"])

    def _dataframe_to_concours(self, df: pl.DataFrame) -> List[Concours]:
        """Convert processed DataFrame back to Concours entities."""
        if len(df) == 0:
            return []

        concours_list: List[Concours] = []
        # for row in df.to_dicts():
        #     category = self._map_category(row["category"])
        #     ministry = self._map_ministry(row["ministry"])
        #     access_modalities = self._map_access_modalities(row["access_mod"])

        #     corps = Concours()
        #     corps_list.append(corps)

        return concours_list

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
        elif "C" in category_upper:
            return Category.C
        else:
            raise InvalidCategoryError(category_upper)

    def _map_ministry(self, ministry_str: Optional[str]) -> Ministry:
        """Map ministry string to Ministry enum."""
        if ministry_str == "Météo France":
            return Ministry.METEO_FRANCE

        return Ministry(ministry_str)

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
