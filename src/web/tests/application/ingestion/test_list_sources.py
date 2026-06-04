from unittest.mock import MagicMock

from tests.factories.ingestion.source_factory import SourceFactory


def test_execute_returns_empty_list_when_no_sources(list_sources_usecase):
    list_sources_usecase.source_repository.get_all = MagicMock(return_value=[])

    result = list_sources_usecase.execute()

    assert result == []
    list_sources_usecase.source_repository.get_all.assert_called_once()


def test_execute_returns_all_sources(list_sources_usecase):
    sources = [SourceFactory.create_entity(), SourceFactory.create_entity()]
    list_sources_usecase.source_repository.get_all = MagicMock(return_value=sources)

    result = list_sources_usecase.execute()

    assert result == sources
    assert len(result) == 2  # noqa: PLR2004
    list_sources_usecase.source_repository.get_all.assert_called_once()


def test_execute_delegates_to_repository(list_sources_usecase):
    list_sources_usecase.source_repository.get_all = MagicMock(return_value=[])

    list_sources_usecase.execute()

    list_sources_usecase.source_repository.get_all.assert_called_once_with()
