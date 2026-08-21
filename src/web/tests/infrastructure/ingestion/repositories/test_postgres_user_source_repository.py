import pytest

from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.ingestion.source_factory import SourceFactory
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


@pytest.fixture(name="repository")
def repository_fixture(ingestion_container):
    return ingestion_container.user_source_repository()


@pytest.fixture(name="utilisateur_with_source")
def utilisateur_with_source_fixture():
    user_model = UtilisateurFactory.create_model()
    source = SourceFactory.create_model()
    user_model.sources.add(source)
    return UtilisateurMapper().to_domain(user_model), source


@pytest.fixture(name="utilisateur_without_source")
def utilisateur_without_source_fixture():
    user_model = UtilisateurFactory.create_model()
    return UtilisateurMapper().to_domain(user_model)


def test_returns_empty_set_when_user_has_no_sources(
    repository, utilisateur_without_source
):
    source = SourceFactory.create_model()

    result = repository.get_allowed_source_ids(
        utilisateur_without_source, {source.source_id}
    )

    assert result == set()


def test_returns_allowed_source_ids_for_user(repository, utilisateur_with_source):
    utilisateur, source = utilisateur_with_source

    result = repository.get_allowed_source_ids(utilisateur, {source.source_id})

    assert result == {source.source_id}


def test_filters_out_sources_not_belonging_to_user(repository, utilisateur_with_source):
    utilisateur, source = utilisateur_with_source
    other_source = SourceFactory.create_model()

    result = repository.get_allowed_source_ids(
        utilisateur, {source.source_id, other_source.source_id}
    )

    assert result == {source.source_id}


def test_returns_empty_set_when_source_ids_is_empty(
    repository, utilisateur_without_source
):
    result = repository.get_allowed_source_ids(utilisateur_without_source, set())

    assert result == set()
