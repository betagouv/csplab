from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from faker import Faker

from config.app_config import AppConfig
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.recruteur.note_factory import NoteFactory
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.recruteur.postgres_note_query_service import (
    PostgresNoteQueryService,
)

fake = Faker("fr_FR")


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="service")
def service_fixture(recruteur_integration_container) -> PostgresNoteQueryService:
    return recruteur_integration_container.postgres_note_query_service()


def test_get_by_candidature_service_returns_ordered_notes(service):
    agent = AgentFactory.create_model()
    note = NoteFactory.create_model(publie_par_id=UUID(agent.utilisateur_id))
    note_recent = NoteFactory.create_model(
        candidature_id=note.candidature_id, publie_par_id=UUID(agent.utilisateur_id)
    )

    notes = service.get_by_candidature(note.candidature_id)

    assert [n.entity_id for n in notes] == [note_recent.id, note.id]
    assert notes[0].publie_par_id == UUID(agent.utilisateur_id)
    assert notes[0].publie_par_prenom == agent.utilisateur.first_name
    assert notes[0].publie_par_nom == agent.utilisateur.last_name


def test_get_by_candidature_service_ignores_soft_deleted_notes(service):
    model = NoteFactory.create_model()
    model.supprimee_le = datetime.now(UTC)
    model.save()

    assert service.get_by_candidature(model.candidature_id) == []


def test_get_by_candidature_service_ignores_unrelated_notes(service):
    NoteFactory.create_model()

    assert service.get_by_candidature(uuid4()) == []
