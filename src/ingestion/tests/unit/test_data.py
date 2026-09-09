import csv

from infrastructure.gateways.transcoding import _DATA_DIR

REQUIRED_TABLES = {
    "categories",
    "departements",
    "metiers",
    "niveaux_de_diplome",
    "niveaux_de_langue",
    "niveaux_d_experience",
    "oui_non",
    "pays",
    "regions",
    "types_de_contrat",
    "verses",
    "zones_geo",
}

REQUIRED_COLUMNS = {"code_client", "mappe_sur_code_client_dgafp"}


def test_each_source_has_the_required_csv_files():
    source_directories = [d for d in _DATA_DIR.iterdir() if d.is_dir()]
    assert source_directories, f"No source directory found under {_DATA_DIR}"

    for source_directory in source_directories:
        present_tables = {csv_path.stem for csv_path in source_directory.glob("*.csv")}
        missing_tables = REQUIRED_TABLES - present_tables
        assert not missing_tables, (
            f"Source '{source_directory.name}' is missing required CSV files: "
            f"{sorted(missing_tables)}"
        )

        for table in REQUIRED_TABLES:
            csv_path = source_directory / f"{table}.csv"
            with csv_path.open(encoding="utf-8") as f:
                fieldnames = set(csv.DictReader(f, delimiter=";").fieldnames or [])
            missing_columns = REQUIRED_COLUMNS - fieldnames
            assert not missing_columns, (
                f"'{csv_path}' is missing required columns: {sorted(missing_columns)}"
            )
