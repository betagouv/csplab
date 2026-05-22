import pytest

from domain.source import Source
from infrastructure.sources_registry import SourcesRegistry


def make_source(client_id_back: str = "back-1", source_id: str = "uuid-1") -> Source:
    return Source(
        source_id=source_id,
        type="talentsoft",
        client_id_front="front-1",
        client_id_back=client_id_back,
        base_url_front="https://front.example.com",
        base_url_back="https://back.example.com",
    )


@pytest.fixture
def registry() -> SourcesRegistry:
    return SourcesRegistry()


def test_empty_registry_has_zero_length(registry: SourcesRegistry):
    assert len(registry) == 0


def test_empty_registry_returns_none_for_any_key(registry: SourcesRegistry):
    assert registry.get_by_client_id_back("unknown") is None


def test_load_returns_source_by_client_id_back(registry: SourcesRegistry):
    source = make_source(client_id_back="back-1", source_id="uuid-1")
    registry.load([source])
    assert registry.get_by_client_id_back("back-1") == source


def test_get_by_client_id_back_returns_none_for_unknown_key(registry: SourcesRegistry):
    registry.load([make_source(client_id_back="back-1")])
    assert registry.get_by_client_id_back("unknown") is None


def test_load_multiple_sources(registry: SourcesRegistry):
    source1 = make_source(client_id_back="back-1", source_id="uuid-1")
    source2 = make_source(client_id_back="back-2", source_id="uuid-2")
    registry.load([source1, source2])
    assert registry.get_by_client_id_back("back-1") == source1
    assert registry.get_by_client_id_back("back-2") == source2
    assert len(registry) == 2


def test_load_replaces_previous_entries(registry: SourcesRegistry):
    registry.load([make_source(client_id_back="back-1", source_id="uuid-1")])
    source2 = make_source(client_id_back="back-2", source_id="uuid-2")
    registry.load([source2])
    assert registry.get_by_client_id_back("back-1") is None
    assert registry.get_by_client_id_back("back-2") == source2
    assert len(registry) == 1
