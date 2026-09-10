import csv
import re
from pathlib import Path

from infrastructure.gateways.transcoding import _DATA_DIR

_OFFERS_CLEANER_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "infrastructure"
    / "gateways"
    / "offers_cleaner.py"
)

REQUIRED_COLUMNS = {"code_client", "mappe_sur_code_client_dgafp"}


def _required_tables() -> set[str]:
    source = _OFFERS_CLEANER_PATH.read_text(encoding="utf-8")
    return set(re.findall(r'transcoder\.translate\(\s*"([^"]+)"', source))


def test_each_source_has_the_required_csv_files():
    required_tables = _required_tables()
    assert required_tables, (
        f"No transcoder.translate(...) call found in {_OFFERS_CLEANER_PATH}"
    )

    source_directories = [d for d in _DATA_DIR.iterdir() if d.is_dir()]
    assert source_directories, f"No source directory found under {_DATA_DIR}"

    for source_directory in source_directories:
        present_tables = {csv_path.stem for csv_path in source_directory.glob("*.csv")}
        missing_tables = required_tables - present_tables
        assert not missing_tables, (
            f"Source '{source_directory.name}' is missing required CSV files: "
            f"{sorted(missing_tables)}"
        )

        for table in required_tables:
            csv_path = source_directory / f"{table}.csv"
            with csv_path.open(encoding="utf-8") as f:
                fieldnames = set(csv.DictReader(f, delimiter=";").fieldnames or [])
            missing_columns = REQUIRED_COLUMNS - fieldnames
            assert not missing_columns, (
                f"'{csv_path}' is missing required columns: {sorted(missing_columns)}"
            )
