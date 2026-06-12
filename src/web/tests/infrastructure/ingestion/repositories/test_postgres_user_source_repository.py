import pytest

from tests.factories.identite.utilisateur_factory import UtilisateurFactory
from tests.factories.ingestion.source_factory import SourceFactory


@pytest.fixture(name="repository")
def repository_fixture(ingestion_container):
    return ingestion_container.user_source_repository()


def test_returns_empty_set_when_user_has_no_sources(repository):
    user_model = UtilisateurFactory.create_model()
    utilisateur = user_model.to_entity()
    source = SourceFactory.create_model()

    result = repository.get_allowed_source_ids(utilisateur, {source.source_id})

    assert result == set()


def test_returns_allowed_source_ids_for_user(repository):
    user_model = UtilisateurFactory.create_model()
    utilisateur = user_model.to_entity()
    allowed_source = SourceFactory.create_model()
    user_model.sources.add(allowed_source)

    result = repository.get_allowed_source_ids(utilisateur, {allowed_source.source_id})

    assert result == {allowed_source.source_id}


def test_filters_out_sources_not_belonging_to_user(repository):
    user_model = UtilisateurFactory.create_model()
    utilisateur = user_model.to_entity()
    allowed_source = SourceFactory.create_model()
    other_source = SourceFactory.create_model()
    user_model.sources.add(allowed_source)

    result = repository.get_allowed_source_ids(
        utilisateur, {allowed_source.source_id, other_source.source_id}
    )

    assert result == {allowed_source.source_id}


def test_returns_empty_set_when_source_ids_is_empty(repository):
    user_model = UtilisateurFactory.create_model()
    utilisateur = user_model.to_entity()

    result = repository.get_allowed_source_ids(utilisateur, set())

    assert result == set()
