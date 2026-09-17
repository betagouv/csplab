from pathlib import Path

from infrastructure.gateways.siret_cache import SiretCsvCache


def test_get_returns_none_when_cache_file_does_not_exist(tmp_path: Path):
    cache = SiretCsvCache(tmp_path / "cache.csv")

    assert cache.get("dila-1") is None


def test_set_then_get_returns_the_cached_value(tmp_path: Path):
    cache = SiretCsvCache(tmp_path / "cache.csv")

    cache.set("dila-1", "26060047300342")

    assert cache.get("dila-1") == "26060047300342"


def test_set_persists_to_disk(tmp_path: Path):
    csv_path = tmp_path / "cache.csv"
    cache = SiretCsvCache(csv_path)

    cache.set("dila-1", "26060047300342")

    reloaded = SiretCsvCache(csv_path)
    assert reloaded.get("dila-1") == "26060047300342"


def test_set_can_cache_an_empty_value_to_avoid_retrying(tmp_path: Path):
    csv_path = tmp_path / "cache.csv"
    cache = SiretCsvCache(csv_path)

    cache.set("dila-1", "")

    assert cache.get("dila-1") == ""
    reloaded = SiretCsvCache(csv_path)
    assert reloaded.get("dila-1") == ""


def test_set_does_not_overwrite_an_existing_entry(tmp_path: Path):
    cache = SiretCsvCache(tmp_path / "cache.csv")
    cache.set("dila-1", "26060047300342")

    cache.set("dila-1", "35600000000048")

    assert cache.get("dila-1") == "26060047300342"


def test_set_creates_parent_directories(tmp_path: Path):
    csv_path = tmp_path / "nested" / "cache.csv"
    cache = SiretCsvCache(csv_path)

    cache.set("dila-1", "26060047300342")

    assert csv_path.exists()
