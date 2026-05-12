"""Concours cleaner adapter."""

from datetime import datetime
from typing import List, Optional

import polars as pl
from django.utils import timezone

from domain.entities.concours import Concours
from domain.entities.document import Document, DocumentType
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.exceptions.corps_errors import InvalidMinistryError
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.services.document_cleaner_interface import CleaningResult, IDocumentCleaner
from domain.services.logger_interface import ILogger
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR

REFERENCE_YEAR = 2024
DECEMBER = 12

COLUMN_RENAME = {
    "N° NOR": "nor",
    "N° NOR de référence": "nor_reference",
    "Ministère": "ministere",
    "Ministère (saisie initiale)": "ministere_initial",
    "Catégorie": "categorie",
    "Corps": "corps",
    "Grade": "grade",
    "Corps/Grade (saisie initiale)": "corps_grade_initial",
    "Direction/Établissement": "direction_etablissement",
    "Année de référence": "annee_reference",
    "Statut": "statut",
    "Date de première épreuve": "date_premiere_epreuve",
    "National": "national",
    "National à affectation locale": "national_affectation_locale",
    "Déconcentré": "deconcentre",
    "Externe": "externe",
    "Interne": "interne",
    "Troisieme Concours": "troisieme_concours",
    "Unique": "unique",
    "Examen professionnel": "examen_professionnel",
    "Sans concours externe": "sans_concours_externe",
    "Pacte": "pacte",
    "Sélection professionnelle": "selection_professionnelle",
    "Concours spécial": "concours_special",
    "Concours réservé": "concours_reserve",
    "Sans concours interne réservé": "sans_concours_interne_reserve",
    "Examen professionnalisé réservé": "examen_professionnalise_reserve",
    "Interne exceptionnel": "interne_exceptionnel",
    "Apprenti BOETH": "apprenti_boeth",
    "Promotion BOETH": "promotion_boeth",
    "Autres": "autres",
    "Nb postes ACVG": "nb_postes_acvg",
    "Nb postes TH": "nb_postes_th",
    "Nb postes total": "nb_postes_total",
}

# Mapping from raw data access modality strings to AccessModality enum values
ACCESS_MODALITY_MAPPING = {
    "Externe": AccessModality.CONCOURS_EXTERNE,
    "Interne": AccessModality.CONCOURS_INTERNE,
    "Troisieme Concours": AccessModality.TROISIEME_CONCOURS,
    "Unique": AccessModality.CONCOURS_UNIQUE,
    "Examen professionnel": AccessModality.EXAMEN_PROFESSIONNEL,
    "Sans concours externe": AccessModality.SANS_CONCOURS,
    "Concours réservé": AccessModality.CONCOURS_RESERVE,
    "Sans concours interne réservé": AccessModality.SANS_CONCOURS,
    "Examen professionnalisé réservé": AccessModality.EXAMEN_PROFESSIONNEL,
    "Interne exceptionnel": AccessModality.CONCOURS_INTERNE_EXCEPT,
    # Valeurs par défaut → AU_CHOIX
    "Pacte": AccessModality.AU_CHOIX,
    "Sélection professionnelle": AccessModality.AU_CHOIX,
    "Concours spécial": AccessModality.AU_CHOIX,
    "Apprenti BOETH": AccessModality.AU_CHOIX,
    "Promotion BOETH": AccessModality.AU_CHOIX,
    "Autres": AccessModality.AU_CHOIX,
}


class ConcoursCleaner(IDocumentCleaner[Concours]):
    def __init__(self, logger: ILogger, concours_repository: IConcoursRepository):
        self.logger = logger
        self.concours_repository = concours_repository

    def clean(self, raw_documents: List[Document]) -> CleaningResult[Concours]:
        if not raw_documents:
            return CleaningResult(entities=[], cleaning_errors=[])

        for document in raw_documents:
            if document.type != DocumentType.CONCOURS:
                raise InvalidDocumentTypeError(document.type.value)

        concours_data = []
        for document in raw_documents:
            concours_data.append(document.raw_data)

        df = pl.DataFrame(concours_data, infer_schema_length=None)

        df = df.rename({k: v for k, v in COLUMN_RENAME.items() if k in df.columns})

        df_filtered = self._apply_filters(df)

        df_processed = self._process_concours_data(df_filtered)

        concours_list = self._dataframe_to_concours(df_processed)

        return CleaningResult(entities=concours_list, cleaning_errors=[])

    def _apply_filters(self, df: pl.DataFrame) -> pl.DataFrame:
        df = df.filter(pl.col("statut") == "VALIDE")
        df = df.filter(pl.col("annee_reference") > REFERENCE_YEAR)
        df = df.filter(pl.col("ministere") != "Ministère des Armées")

        required_cols = ["nor", "annee_reference", "corps", "categorie"]

        for col in required_cols:
            df = df.filter(pl.col(col).is_not_null())
        return df

    def _process_concours_data(self, df: pl.DataFrame) -> pl.DataFrame:
        df = df.with_columns(
            [
                pl.when(pl.col("nor_reference").is_not_null())
                .then(pl.col("nor_reference"))
                .otherwise(pl.col("nor"))
                .alias("concours_id_temp")
            ]
        )

        multi_corps_ids = (
            df.group_by("concours_id_temp")
            .agg(pl.col("corps").n_unique().alias("nb_corps"))
            .filter(pl.col("nb_corps") > 1)
            .select("concours_id_temp")
            .to_series()
            .to_list()
        )

        df = df.with_columns(
            [
                pl.when(pl.col("concours_id_temp").is_in(multi_corps_ids))
                .then(pl.col("nor"))
                .otherwise(pl.col("concours_id_temp"))
                .alias("concours_id")
            ]
        ).drop("concours_id_temp")

        df = df.with_columns(
            [
                pl.col("nor")
                .map_elements(self._extract_nor_sort_key, return_dtype=pl.Int64)
                .alias("nor_sort_key")
            ]
        )

        df_dedup = (
            df.sort("nor_sort_key", descending=True)
            .group_by("concours_id")
            .agg([pl.all().first(), pl.col("nor").alias("all_nors_in_concours")])
            .drop("nor_sort_key")
        )

        access_modality_cols = [
            "externe",
            "interne",
            "troisieme_concours",
            "unique",
            "examen_professionnel",
            "sans_concours_externe",
            "pacte",
            "selection_professionnelle",
            "concours_special",
            "concours_reserve",
            "sans_concours_interne_reserve",
            "examen_professionnalise_reserve",
            "interne_exceptionnel",
            "apprenti_boeth",
            "promotion_boeth",
            "autres",
        ]

        col_to_label = {v: k for k, v in COLUMN_RENAME.items()}

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
                        .then(pl.lit(col_to_label[col]))
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
                "ministere",
                "categorie",
                "corps",
                "grade",
                "all_nors_in_concours",
                "nb_postes_total",
                "date_premiere_epreuve",
                "mod_access",
            ]
        )

        return df_final

    def _dataframe_to_concours(self, df: pl.DataFrame) -> List[Concours]:
        if len(df) == 0:
            return []

        concours_list: List[Concours] = []
        counter = 0
        for row in df.to_dicts():
            category = self._map_category(row["categorie"])
            if category is None:
                self.logger.warning(
                    f"Catégorie manquante pour {row.get('concours_id', 'unknown')}"
                )
                continue

            ministry = self._map_ministry(row["ministere"])
            access_modalities = self._map_access_modalities(row["mod_access"])

            nor_original = NOR(row["concours_id"])
            nor_list = [NOR(nor) for nor in row["all_nors_in_concours"]]

            written_exam_date = self._parse_date(row.get("date_premiere_epreuve"))

            open_position_number = int(row.get("nb_postes_total", 0) or 0)

            concours = Concours(
                nor_original=nor_original,
                nor_list=nor_list,
                category=category,
                ministry=ministry,
                access_modality=access_modalities,
                corps=row["corps"],
                grade=row.get("grade") or "",
                written_exam_date=written_exam_date,
                open_position_number=open_position_number,
            )
            # Check if Concours with this NOR already exists
            try:
                existing_concours = self.concours_repository.get_by_nor(nor_original)
                concours.id = existing_concours.id
            except ConcoursDoesNotExist:
                self.logger.info(
                    "Creating new Concours with NOR %s", nor_original.value
                )
            concours_list.append(concours)
            counter += 1  # Increment counter for next concours

        return concours_list

    def _extract_nor_sort_key(self, nor_value: str) -> int:
        if not nor_value or len(nor_value) != DECEMBER:
            return 0
        try:
            year = int(nor_value[4:6])
            sequence = int(nor_value[6:11])
            return year * 100000 + sequence
        except (ValueError, IndexError):
            return 0

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return timezone.make_aware(datetime.strptime(date_str, "%d/%m/%Y"))
        except (ValueError, TypeError):
            return None

    def _map_category(self, category_str: Optional[str]) -> Optional[Category]:
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
            return Category.HORS_CATEGORIE

    def _map_ministry(self, ministry_str: Optional[str]) -> Ministry:
        if not ministry_str:
            raise InvalidMinistryError("Unknown minnistry")

        # Direct mappings for known ministry names
        ministry_mappings = {
            "Météo France": Ministry.METEO_FRANCE,
            "Ministère de la Culture": Ministry.MC,
            "Ministère de l'Europe et des Affaires Etrangères": Ministry.MEAE,
            "Premier ministre": Ministry.PREMIER_MINISTRE,
            "Ministère de l'Économie, des Finances et de la Souveraineté industrielle et numérique": Ministry.MEF,  # noqa: E501
            "Ministère de l'Agriculture et de la Souveraineté alimentaire": Ministry.MAA,  # noqa: E501
            "Ministère de la Transition écologique et de la Cohésion des territoires": Ministry.MTE,  # noqa: E501
            "Ministère de l'Enseignement supérieur et de la Recherche": Ministry.MESRI,
            "Ministère de l'Education Nationale et de la Jeunesse": Ministry.MEN,
            "Ministère du Travail, du Plein emploi et de l'Insertion": Ministry.MTEI,
            "Ministère de la Justice": Ministry.MJ,
            "Ministère Solidarités et Santé": Ministry.MSS,
            "Ministère de l'Intérieur et des Outre-mer": Ministry.MI,
            "Conseil d'Etat": Ministry.CONSEIL_ETAT,
            "Caisse des Dépôts et Consignations": Ministry.CAISSE_DES_DEPOTS_ET_CONSIGNATIONS,  # noqa: E501
            "Cour des comptes": Ministry.COUR_COMPTES,
        }

        if ministry_str in ministry_mappings:
            return ministry_mappings[ministry_str]
        else:
            raise InvalidMinistryError("Unknown minnistry")

    def _map_access_modalities(
        self, access_mod_list: List[str]
    ) -> List[AccessModality]:
        modalities = []
        for mod_str in access_mod_list:
            # Use mapping dictionary, default to AU_CHOIX if not found
            modality = ACCESS_MODALITY_MAPPING.get(mod_str, AccessModality.AU_CHOIX)
            modalities.append(modality)

        return modalities
