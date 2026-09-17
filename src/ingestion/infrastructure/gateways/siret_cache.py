import csv
import threading
from pathlib import Path

_FIELDNAMES = ["external_id", "siret"]


class SiretCsvCache:
    def __init__(self, csv_path: Path) -> None:
        self._csv_path = csv_path
        self._lock = threading.Lock()
        self._entries = self._load()

    def _load(self) -> dict[str, str]:
        if not self._csv_path.exists():
            return {}
        with self._csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return {row["external_id"]: row["siret"] for row in reader}

    def get(self, external_id: str) -> str | None:
        return self._entries.get(external_id)

    def set(self, external_id: str, siret: str) -> None:
        with self._lock:
            if external_id in self._entries:
                return
            self._entries[external_id] = siret
            is_new_file = not self._csv_path.exists()
            self._csv_path.parent.mkdir(parents=True, exist_ok=True)
            with self._csv_path.open("a", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
                if is_new_file:
                    writer.writeheader()
                writer.writerow({"external_id": external_id, "siret": siret})
