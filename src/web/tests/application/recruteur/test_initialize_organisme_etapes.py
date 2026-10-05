from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from application.recruteur.services.initialize_organisme_etapes import (
    initialize_organisme_etapes,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

NB_ETAPES_PAR_DEFAUT = 6


def _audit_logs(organisme_id):
    return PostgresAuditLogRepository().get_logs_for_ressource(
        "OrganismeRecruteur", organisme_id
    )


def test_superviseur_replaces_etapes_with_defaults(db):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR,
        etapes=EtapeRecrutementFactory.create_entity_batch(),
    )
    anciens_ids = {e["entity_id"] for e in organisme.etapes}

    result = initialize_organisme_etapes(
        organisme_id=organisme.id, utilisateur=agent.utilisateur
    )

    organisme.refresh_from_db()
    assert organisme.etapes == result.etapes
    assert len(organisme.etapes) == NB_ETAPES_PAR_DEFAUT
    assert anciens_ids.isdisjoint(e["entity_id"] for e in organisme.etapes)


def test_staff_without_liaison_initializes_etapes(db):
    organisme = OrganismeDjangoFactory()
    staff = UtilisateurDjangoFactory(is_staff=True)

    initialize_organisme_etapes(organisme_id=organisme.id, utilisateur=staff)

    organisme.refresh_from_db()
    assert len(organisme.etapes) == NB_ETAPES_PAR_DEFAUT


def test_logs_action(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)

    initialize_organisme_etapes(
        organisme_id=organisme.id, utilisateur=agent.utilisateur
    )

    logs = _audit_logs(organisme.id)
    assert len(logs) == 1
    assert logs[0].event_name == "OrganismeEtapesInitialises"
    assert logs[0].utilisateur_id == agent.utilisateur.username
    assert logs[0].ressource_id == organisme.id


def test_updated_at_advances(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    updated_at_avant = organisme.updated_at

    initialize_organisme_etapes(
        organisme_id=organisme.id, utilisateur=agent.utilisateur
    )

    organisme.refresh_from_db()
    assert organisme.updated_at > updated_at_avant


def test_membre_is_denied_without_audit(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

    with pytest.raises(AccesOrganismeRefuse):
        initialize_organisme_etapes(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

    organisme.refresh_from_db()
    assert organisme.etapes is None
    assert _audit_logs(organisme.id) == []


def test_superviseur_of_another_organisme_is_denied_without_audit(db):
    organisme = OrganismeDjangoFactory()
    autre_superviseur, _ = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )

    with pytest.raises(AccesOrganismeRefuse):
        initialize_organisme_etapes(
            organisme_id=organisme.id, utilisateur=autre_superviseur.utilisateur
        )

    organisme.refresh_from_db()
    assert organisme.etapes is None
    assert _audit_logs(organisme.id) == []


def test_unknown_organisme_raises(db):
    with pytest.raises(OrganismeNexistePas):
        initialize_organisme_etapes(
            organisme_id=uuid4(), utilisateur=UtilisateurDjangoFactory(is_staff=True)
        )


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_when_audit_log_fails(db):
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR,
        etapes=EtapeRecrutementFactory.create_entity_batch(),
    )
    organisme.refresh_from_db()
    etapes_avant, updated_at_avant = organisme.etapes, organisme.updated_at

    with pytest.raises(RuntimeError):
        initialize_organisme_etapes(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

    organisme.refresh_from_db()
    assert organisme.etapes == etapes_avant
    assert organisme.updated_at == updated_at_avant


def test_does_not_log_when_save_fails(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)

    with (
        patch.object(OrganismeModel, "save", side_effect=RuntimeError("save failed")),
        pytest.raises(RuntimeError),
    ):
        initialize_organisme_etapes(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

    assert _audit_logs(organisme.id) == []
