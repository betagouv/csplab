import pytest
from referentiel.entities.source import Source
from referentiel.value_objects.source_type import SourceType

from infrastructure.sources_repository import SourcesRepository


def make_source(client_id_back: str = "back-1", source_id: str = "uuid-1") -> Source:
    return Source(
        source_id=source_id,
        slug="source-slug",
        type=SourceType.TALENTSOFT,
        client_id_front="front-1",
        client_id_back=client_id_back,
        base_url_front="https://front.example.com",
        base_url_back="https://back.example.com",
    )


@pytest.fixture
def repository() -> SourcesRepository:
    return SourcesRepository()


def test_empty_repository_has_zero_length(repository: SourcesRepository):
    assert len(repository) == 0


def test_empty_repository_returns_none_for_any_key(repository: SourcesRepository):
    assert repository.get_by_client_id_back("unknown") is None


def test_load_returns_source_by_client_id_back(repository: SourcesRepository):
    source = make_source(client_id_back="back-1", source_id="uuid-1")
    repository.load([source])
    assert repository.get_by_client_id_back("back-1") == source


def test_get_by_client_id_back_returns_none_for_unknown_key(
    repository: SourcesRepository,
):
    repository.load([make_source(client_id_back="back-1")])
    assert repository.get_by_client_id_back("unknown") is None


def test_load_multiple_sources(repository: SourcesRepository):
    source1 = make_source(client_id_back="back-1", source_id="uuid-1")
    source2 = make_source(client_id_back="back-2", source_id="uuid-2")
    repository.load([source1, source2])
    assert repository.get_by_client_id_back("back-1") == source1
    assert repository.get_by_client_id_back("back-2") == source2
    assert len(repository) == 2


def test_load_replaces_previous_entries(repository: SourcesRepository):
    repository.load([make_source(client_id_back="back-1", source_id="uuid-1")])
    source2 = make_source(client_id_back="back-2", source_id="uuid-2")
    repository.load([source2])
    assert repository.get_by_client_id_back("back-1") is None
    assert repository.get_by_client_id_back("back-2") == source2
    assert len(repository) == 1
