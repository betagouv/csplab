import pytest

from tests.factories.identite.utilisateur_factory import UtilisateurFactory
from tests.factories.ingestion.source_factory import SourceFactory


@pytest.fixture(name="repository")
def repository_fixture(ingestion_container):
    return ingestion_container.user_source_repository()


def test_returns_empty_set_when_user_has_no_sources(repository):
    user = UtilisateurFactory.create_model()
    source = SourceFactory.create_model()

    result = repository.get_allowed_source_ids(user, {source.source_id})

    assert result == set()


def test_returns_allowed_source_ids_for_user(repository):
    user = UtilisateurFactory.create_model()
    allowed_source = SourceFactory.create_model()
    user.sources.add(allowed_source)

    result = repository.get_allowed_source_ids(user, {allowed_source.source_id})

    assert result == {allowed_source.source_id}


def test_filters_out_sources_not_belonging_to_user(repository):
    user = UtilisateurFactory.create_model()
    allowed_source = SourceFactory.create_model()
    other_source = SourceFactory.create_model()
    user.sources.add(allowed_source)

    result = repository.get_allowed_source_ids(
        user, {allowed_source.source_id, other_source.source_id}
    )

    assert result == {allowed_source.source_id}


def test_returns_empty_set_when_source_ids_is_empty(repository):
    user = UtilisateurFactory.create_model()

    result = repository.get_allowed_source_ids(user, set())

    assert result == set()
