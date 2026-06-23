from referentiel.value_objects.source_type import SourceType

from tests.factories.ingestion.source_factory import SourceFactory


def test_returns_empty_list_when_no_sources(ingestion_container):
    result = ingestion_container.list_sources_usecase().execute()

    assert result == []


def test_returns_all_sources(ingestion_container):
    SourceFactory.create_model()
    SourceFactory.create_model()

    result = ingestion_container.list_sources_usecase().execute()

    assert len(result) == 2  # noqa: PLR2004


def test_returns_correct_source_entity_fields(ingestion_container):
    model = SourceFactory.create_model(
        type=SourceType.TALENTSOFT,
        client_id_front="my_front_id",
        client_id_back="my_back_id",
    )

    result = ingestion_container.list_sources_usecase().execute()

    assert len(result) == 1
    source = result[0]
    assert source.source_id == model.source_id
    assert source.type == SourceType.TALENTSOFT
    assert source.client_id_front == "my_front_id"
    assert source.client_id_back == "my_back_id"
    assert source.base_url_front == model.base_url_front
    assert source.base_url_back == model.base_url_back
