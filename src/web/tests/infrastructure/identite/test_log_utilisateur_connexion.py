import pytest

from application.identite.usecases.log_utilisateur_connexion import (
    LogUtilisateurConnexionInput,
)
from config.app_config import AppConfig
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.utilisateur_factory import UtilisateurFactory


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_records_authentication_against_the_utilisateur(identite_integration_container):
    utilisateur = UtilisateurFactory.create_entity()

    identite_integration_container.log_utilisateur_connexion_usecase().execute(
        LogUtilisateurConnexionInput(utilisateur=utilisateur)
    )

    audit_log_repository = (
        identite_integration_container.postgres_audit_log_repository()
    )
    logs = audit_log_repository.get_logs_for_ressource(
        "Utilisateur", utilisateur.entity_id
    )
    assert len(logs) == 1
    log = logs[0]
    assert log.ressource_kind == "Utilisateur"
    assert log.event_name == "Connexion"
    assert log.utilisateur_id == utilisateur.entity_id
    assert log.ressource_id == utilisateur.entity_id
    assert log.event_id is None
