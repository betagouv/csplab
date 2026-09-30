from unittest.mock import Mock, patch

import pytest
from faker import Faker

from application.identite.usecases.create_candidat import CreateCandidatInput
from config.app_config import AppConfig
from domain.identite.errors.candidat_errors import ProfilCandidatExisteDeja
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.identite.postgres_candidat_repository import (
    PostgresCandidatRepository,
)

fake = Faker()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def _candidat_logs(container, ressource_id):
    return container.postgres_audit_log_repository().get_logs_for_ressource(
        "Candidat", ressource_id
    )


def test_create_candidat_normalizes_the_email(identite_integration_container):
    input_data = CreateCandidatInput(
        email="  Marie.MARTIN@GOUV.FR  ",
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    result = identite_integration_container.create_candidat_usecase().execute(
        input_data
    )

    assert result.email == "marie.martin@gouv.fr"


def test_create_candidat(identite_integration_container):
    input_data = CreateCandidatInput(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    result = identite_integration_container.create_candidat_usecase().execute(
        input_data
    )

    assert result.email == input_data.email
    assert result.prenom == input_data.prenom
    assert result.nom == input_data.nom
    assert result.resume == input_data.resume
    [log] = _candidat_logs(identite_integration_container, result.entity_id)
    assert log.event_name == "ProfilCandidatCree"
    assert log.utilisateur_id == result.entity_id


def test_create_candidat_with_existing_user(identite_integration_container):
    existing_user = UtilisateurDjangoFactory(email=fake.email())
    input_data = CreateCandidatInput(
        email=existing_user.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    result = identite_integration_container.create_candidat_usecase().execute(
        input_data
    )

    assert result.entity_id == existing_user.username
    [log] = _candidat_logs(identite_integration_container, existing_user.username)
    assert log.event_name == "ProfilCandidatCree"
    assert log.utilisateur_id == existing_user.username


def test_cannot_create_candidat_twice(identite_integration_container):
    existing_candidat = CandidatDjangoFactory()
    input_data = CreateCandidatInput(
        email=existing_candidat.utilisateur.email,
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    with pytest.raises(ProfilCandidatExisteDeja):
        identite_integration_container.create_candidat_usecase().execute(input_data)

    assert not AuditLogModel.objects.exists()


@patch.object(
    PostgresCandidatRepository,
    "create",
    new=Mock(side_effect=RuntimeError("write failed")),
)
def test_create_candidat_does_not_log_when_write_fails(
    identite_integration_container,
):
    input_data = CreateCandidatInput(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    with pytest.raises(RuntimeError):
        identite_integration_container.create_candidat_usecase().execute(input_data)

    assert not AuditLogModel.objects.exists()
