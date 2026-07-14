from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from django.db.models.query import QuerySet
from faker import Faker

from config.app_config import AppConfig
from domain.recruteur.errors.note_errors import NoteIntrouvable
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.note_mapper import NoteMapper
from infrastructure.repositories.recruteur.postgres_note_repository import (
    PostgresNoteRepository,
)
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.recruteur.note_factory import NoteFactory

fake = Faker("fr_FR")


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="repository")
def repository_fixture(recruteur_integration_container) -> PostgresNoteRepository:
    return recruteur_integration_container.postgres_note_repository()


@pytest.fixture(name="candidature_id")
def candidature_id_fixture(db) -> UUID:
    return CandidatureFactory.create_model().id


@pytest.fixture(name="agent_id")
def agent_id_fixture(db) -> str:
    return AgentFactory.create_model().utilisateur_id


@pytest.fixture(name="existing_note_model")
def existing_note_model_fixture(candidature_id, agent_id) -> NoteModel:
    return NoteFactory.create_model(
        candidature_id=candidature_id, publie_par_id=agent_id
    )


@pytest.fixture(name="note_save_raises_db_error")
def note_save_raises_db_error_fixture(monkeypatch) -> None:
    monkeypatch.setattr(NoteModel, "save", MagicMock(side_effect=Exception("db error")))
    monkeypatch.setattr(
        QuerySet, "update", MagicMock(side_effect=Exception("db error"))
    )


class TestCreateNote:
    def test_create_note(self, repository, candidature_id, agent_id) -> None:
        note = NoteFactory.create_entity(
            candidature_id=candidature_id, publie_par_id=agent_id
        )

        repository.create(note)

        note_model = NoteModel.objects.get()

        assert note_model.id == note.entity_id
        assert str(note_model.candidature_id) == candidature_id
        assert str(note_model.publie_par_id) == agent_id
        assert note_model.message == note.message

    def test_create_note_propagates_unhandled_db_error(
        self, note_save_raises_db_error, repository, candidature_id, agent_id
    ):
        note = NoteFactory.create_entity(
            candidature_id=candidature_id, publie_par_id=agent_id
        )

        with pytest.raises(Exception, match="db error"):
            repository.create(note)


class TestGetById:
    def test_get_by_id_returns_note(
        self, repository, existing_note_model, candidature_id, agent_id
    ):
        fetched = repository.get_by_id(existing_note_model.id)

        assert fetched.entity_id == existing_note_model.id
        assert str(fetched.candidature_id) == candidature_id
        assert str(fetched.publie_par_id) == agent_id
        assert fetched.message == existing_note_model.message

    def test_get_by_id_does_not_return_soft_deleted_note(
        self, repository, existing_note_model
    ):
        existing_note_model.supprimee_le = datetime.now()
        existing_note_model.save()

        with pytest.raises(NoteIntrouvable):
            repository.get_by_id(existing_note_model.id)

    def test_get_by_id_raises_note_introuvable(self, repository):
        with pytest.raises(NoteIntrouvable):
            repository.get_by_id(uuid4())

    def test_get_by_id_propagates_unhandled_db_error(self, monkeypatch, repository):
        monkeypatch.setattr(
            NoteModel.objects, "get", MagicMock(side_effect=Exception("db error"))
        )

        with pytest.raises(Exception, match="db error"):
            repository.get_by_id(uuid4())


class TestSave:
    def test_save_persists_update(self, repository, existing_note_model):
        current_updated_at = existing_note_model.updated_at
        mapper = NoteMapper()
        note = mapper.to_domain(existing_note_model)

        nouveau_message = fake.sentence()
        note.modifier(message=nouveau_message)
        repository.save(note)

        existing_note_model.refresh_from_db()

        assert existing_note_model.message == nouveau_message
        assert existing_note_model.updated_at > current_updated_at

    def test_save_propagates_unhandled_db_error(
        self, repository, existing_note_model, note_save_raises_db_error
    ):
        mapper = NoteMapper()
        note = mapper.to_domain(existing_note_model)

        with pytest.raises(Exception, match="db error"):
            repository.save(note)


class TestDelete:
    def test_delete_keeps_row(self, repository, existing_note_model):
        current_updated_at = existing_note_model.updated_at
        repository.delete(existing_note_model.id)

        existing_note_model.refresh_from_db()
        assert existing_note_model.supprimee_le is not None
        assert existing_note_model.updated_at > current_updated_at

    def test_delete_propagates_unhandled_db_error(
        self, repository, existing_note_model, note_save_raises_db_error
    ):
        with pytest.raises(Exception, match="db error"):
            repository.delete(existing_note_model.id)
