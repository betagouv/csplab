from unittest.mock import Mock, patch

import pytest
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.initialize_organisme_etapes import (
    initialize_organisme_etapes,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
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


def _audit_logs(organisme_id):
    return PostgresAuditLogRepository().get_logs_for_ressource(
        "OrganismeRecruteur", organisme_id
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


@patch.object(OrganismePermissionService, "can_execute")
def test_supprime_organisme_after_permission_check_raises(_can_execute, db):
    organisme = OrganismeDjangoFactory(supprime_le=timezone.now())

    with pytest.raises(OrganismeNexistePas) as error:
        initialize_organisme_etapes(
            organisme_id=organisme.id, utilisateur=UtilisateurDjangoFactory()
        )

    assert isinstance(error.value.__cause__, OrganismeModel.DoesNotExist)
    organisme.refresh_from_db()
    assert organisme.etapes is None
    assert _audit_logs(organisme.id) == []
