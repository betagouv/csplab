"""Concours cleaner adapter."""

from datetime import datetime
from typing import List, Optional

import polars as pl

from core.entities.concours import Concours
from core.entities.document import Document, DocumentType
from core.errors.corps_errors import InvalidAccessModalityError, InvalidCategoryError
from core.errors.document_error import InvalidDocumentTypeError
from core.services.document_cleaner_interface import IDocumentCleaner
from core.services.logger_interface import ILogger
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry
from core.value_objects.nor import NOR

REFERENCE_YEAR = 2024
DECEMBER = 12


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

        if not raw_documents:
            return []

        concours_data = []
        for document in raw_documents:
            parsed_data = self._parse_concours_data(document.raw_data)
            if parsed_data:
                concours_data.append(parsed_data)

        if not concours_data:
            return []

        df = pl.DataFrame(concours_data)
        self.logger.info(f"Données initiales: {len(df)} lignes")

        df_filtered = self._apply_filters(df)
        self.logger.info(f"Après filtrage: {len(df_filtered)} lignes")

        df_processed = self._process_concours_data(df_filtered)
        self.logger.info(f"Après traitement: {len(df_processed)} lignes")

        return self._dataframe_to_concours(df_processed)

    def _parse_concours_data(self, raw_data: dict) -> Optional[dict]:
        """Parse raw concours data into structured format."""
        return raw_data

    def _apply_filters(self, df: pl.DataFrame) -> pl.DataFrame:
        """Apply filters based on notebook logic."""
        df = df.filter(pl.col("Statut") == "VALIDE")
        df = df.filter(pl.col("Année de référence") > REFERENCE_YEAR)

        required_cols = ["N° NOR", "Année de référence", "Corps", "Catégorie"]
        for col in required_cols:
            df = df.filter(pl.col(col).is_not_null())
        return df

    def _process_concours_data(self, df: pl.DataFrame) -> pl.DataFrame:
        """Process concours data with deduplication and aggregation."""
        # Step 1: create concours_id_temp
        df = df.with_columns(
            [
                pl.when(pl.col("N° NOR de référence").is_not_null())
                .then(pl.col("N° NOR de référence"))
                .otherwise(pl.col("N° NOR"))
                .alias("concours_id_temp")
            ]
        )

        # Step 2: Identify concours_id with several corps
        multi_corps_ids = (
            df.group_by("concours_id_temp")
            .agg(pl.col("Corps").n_unique().alias("nb_corps"))
            .filter(pl.col("nb_corps") > 1)
            .select("concours_id_temp")
            .to_series()
            .to_list()
        )

        # Step 3: create concours_id final
        df = df.with_columns(
            [
                pl.when(pl.col("concours_id_temp").is_in(multi_corps_ids))
                .then(pl.col("N° NOR"))
                .otherwise(pl.col("concours_id_temp"))
                .alias("concours_id")
            ]
        ).drop("concours_id_temp")

        # Step 4: Add NOR sort key for chronological ordering
        df = df.with_columns(
            [
                pl.col("N° NOR")
                .map_elements(self._extract_nor_sort_key, return_dtype=pl.Int64)
                .alias("nor_sort_key")
            ]
        )

        # Step 5: Deduplication and aggregation
        df_dedup = (
            df.sort("nor_sort_key", descending=True)
            .group_by("concours_id")
            .agg([pl.all().first(), pl.col("N° NOR").alias("all_nors_in_concours")])
            .drop("nor_sort_key")
        )

        # Step 6: Process access modalities
        access_modality_cols = [
            "Externe",
            "Interne",
            "Troisieme Concours",
            "Unique",
            "Examen professionnel",
            "Sans concours externe",
            "Pacte",
            "Sélection professionnelle",
            "Concours spécial",
            "Concours réservé",
            "Sans concours interne réservé",
            "Examen professionnalisé réservé",
            "Interne exceptionnel",
            "Apprenti BOETH",
            "Promotion BOETH",
            "Autres",
        ]

        df_final = df_dedup.with_columns(
            [
                pl.concat_list(
                    [
                        pl.when(
                            (pl.col(col).is_not_null())
                            & (pl.col(col).cast(pl.Utf8) != "0")
                            & (pl.col(col).cast(pl.Utf8) != "")
                            & (pl.col(col).cast(pl.Utf8) != "null")
                        )
                        .then(pl.lit(col))
                        .otherwise(None)
                        for col in access_modality_cols
                    ]
                )
                .list.drop_nulls()
                .alias("mod_access")
            ]
        )

        df_final = df_final.select(
            [
                "concours_id",
                "Ministère",
                "Catégorie",
                "Corps",
                "all_nors_in_concours",
                "Nb postes total",
                "Date de première épreuve",
                "mod_access",
            ]
        )

        return df_final

    def _dataframe_to_concours(self, df: pl.DataFrame) -> List[Concours]:
        """Convert processed DataFrame back to Concours entities."""
        if len(df) == 0:
            return []

        concours_list: List[Concours] = []
        for row in df.to_dicts():
            try:
                category = self._map_category(row["Catégorie"])
                if category is None:
                    self.logger.warning(
                        f"Catégorie manquante pour {row.get('concours_id', 'unknown')}"
                    )
                    continue

                ministry = self._map_ministry(row["Ministère"])
                access_modalities = self._map_access_modalities(row["mod_access"])

                nor_original = NOR(row["concours_id"])
                nor_list = [NOR(nor) for nor in row["all_nors_in_concours"]]

                # Parse date
                written_exam_date = self._parse_date(
                    row.get("Date de première épreuve")
                )

                # Parse position number
                open_position_number = int(row.get("Nb postes total", 0) or 0)

                # TODO: Get corps_id from vector matching service
                corps_id = 1  # Placeholder until vector matching is implemented

                concours = Concours(
                    id=0,  # Will be set by repository
                    nor_original=nor_original,
                    nor_list=nor_list,
                    category=category,
                    ministry=ministry,
                    access_modality=access_modalities,
                    corps_id=corps_id,
                    written_exam_date=written_exam_date,
                    open_position_number=open_position_number,
                )
                concours_list.append(concours)

            except Exception as e:
                self.logger.error(f"Erreur {row.get('concours_id', 'unknown')}: {e}")
                continue

        return concours_list

    def _extract_nor_sort_key(self, nor_value: str) -> int:
        """Extract sorting key from NOR for chronological ordering."""
        if not nor_value or len(nor_value) != DECEMBER:
            return 0
        try:
            year = int(nor_value[4:6])
            sequence = int(nor_value[6:11])
            return year * 100000 + sequence
        except (ValueError, IndexError):
            return 0

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None
        try:
            # Assume format DD/MM/YYYY or similar
            return datetime.strptime(date_str, "%d/%m/%Y")
        except (ValueError, TypeError):
            return None

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
