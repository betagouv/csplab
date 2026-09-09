"""Per-Source transcoding tables.

Each TalentSoft Source can use its own vocabulary of ``clientCode`` values
(contract types, education levels, etc.). Rather than hardcoding a given
Source's codes in :class:`OffersCleaner`, its raw code -> canonical code
mapping is described declaratively as CSV files under
``data/<source-slug>/<field>.csv``, one row per code, with columns:

- ``code_client``: the Source's raw code (as sent in the TalentSoft payload)
- ``mappe_sur_code_client_dgafp``: the canonical/DGAFP code that the rest of
  :class:`OffersCleaner` already knows how to map to a domain value.

Add support for a new Source by dropping a new ``data/<slug>/`` directory
with the relevant CSV files; no code change is required to load it. Each
``data/<slug>/`` directory documents, in its own README, which of its CSVs
are actually consulted by :class:`OffersCleaner` (see ``data/ars/README.md``).
"""

import csv
from pathlib import Path
from typing import Optional

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

_TARGET_COLUMN = "mappe_sur_code_client_dgafp"


class SourceTranscoder:
    def __init__(self, tables: dict[str, dict[str, str]]) -> None:
        self._tables = tables

    def translate(self, field: str, code: str) -> Optional[str]:
        return self._tables.get(field, {}).get(code)

    @classmethod
    def from_directory(cls, directory: Path) -> "SourceTranscoder":
        tables = {
            csv_path.stem: _load_table(csv_path)
            for csv_path in sorted(directory.glob("*.csv"))
        }
        return cls(tables)


def _load_table(csv_path: Path) -> dict[str, str]:
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        if _TARGET_COLUMN not in (reader.fieldnames or []):
            return {}
        return {
            row["code_client"]: row[_TARGET_COLUMN]
            for row in reader
            if row.get("code_client") and row.get(_TARGET_COLUMN)
        }


def load_transcoders_by_slug(
    data_dir: Path = _DATA_DIR,
) -> dict[str, SourceTranscoder]:
    return {
        directory.name: SourceTranscoder.from_directory(directory)
        for directory in sorted(data_dir.iterdir())
        if directory.is_dir()
    }
