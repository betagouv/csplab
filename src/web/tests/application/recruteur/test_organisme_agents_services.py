import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch

import pytest
from django.db import connection, connections
from django.utils import timezone

from application.recruteur.services.attach_organisme_agent import (
    attach_organisme_agent,
)
from application.recruteur.services.revoke_organisme_agent import (
    revoke_organisme_agent,
)
from application.recruteur.services.update_organisme_agent import (
    update_organisme_agent,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.errors.organisme_agent_errors import AgentDejaRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    create_organisme_with_agent,
)

audit_log_fails = patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)


def _organisme_with_agent(*, revoked_at=None):
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    liaison = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=AgentOrganismeRole.AGENT.value,
        date_revocation=revoked_at,
    )
    return superviseur.utilisateur, organisme, liaison


@audit_log_fails
def test_attach_rolls_back_creation_when_audit_fails(db):
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    bare_agent = AgentDjangoFactory()

    with pytest.raises(RuntimeError):
        attach_organisme_agent(
            organisme_id=organisme.id,
            agent_id=bare_agent.utilisateur_id,
            role=AgentOrganismeRole.AGENT,
            utilisateur=superviseur.utilisateur,
        )

    assert not OrganismeAgentModel.objects.filter(
        agent_id=bare_agent.utilisateur_id
    ).exists()
    assert not AuditLogModel.objects.exists()


@audit_log_fails
def test_attach_rolls_back_reactivation_when_audit_fails(db):
    revoked_at = timezone.now()
    superviseur, organisme, liaison = _organisme_with_agent(revoked_at=revoked_at)

    with pytest.raises(RuntimeError):
        attach_organisme_agent(
            organisme_id=organisme.id,
            agent_id=liaison.agent_id,
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=superviseur,
        )

    liaison.refresh_from_db()
    assert liaison.role == AgentOrganismeRole.AGENT.value
    assert liaison.date_revocation == revoked_at


@audit_log_fails
def test_update_rolls_back_role_when_audit_fails(db):
    superviseur, organisme, liaison = _organisme_with_agent()

    with pytest.raises(RuntimeError):
        update_organisme_agent(
            organisme_id=organisme.id,
            agent_id=liaison.agent_id,
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=superviseur,
        )

    liaison.refresh_from_db()
    assert liaison.role == AgentOrganismeRole.AGENT.value


@audit_log_fails
def test_revoke_rolls_back_revocation_when_audit_fails(db):
    superviseur, organisme, liaison = _organisme_with_agent()

    with pytest.raises(RuntimeError):
        revoke_organisme_agent(
            organisme_id=organisme.id,
            agent_id=liaison.agent_id,
            utilisateur=superviseur,
        )

    liaison.refresh_from_db()
    assert liaison.date_revocation is None


def _a_lock_waiter_appears(*, within=5.0):
    deadline = time.monotonic() + within
    while time.monotonic() < deadline:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM pg_stat_activity"
                " WHERE datname = current_database() AND wait_event_type = 'Lock'"
                " AND pid <> pg_backend_pid()"
            )
            if cursor.fetchone()[0]:
                return True
        time.sleep(0.01)
    return False


# Course du ticket #2476 : une réactivation validée pendant le rattachement.
def test_attach_waits_for_a_concurrent_reactivation_then_refuses(transactional_db):
    superviseur, organisme, liaison = _organisme_with_agent(revoked_at=timezone.now())

    def attach():
        try:
            return attach_organisme_agent(
                organisme_id=organisme.id,
                agent_id=liaison.agent_id,
                role=AgentOrganismeRole.AGENT,
                utilisateur=superviseur,
            )
        finally:
            connection.close()

    with ThreadPoolExecutor(max_workers=1) as executor:
        concurrente = connections.create_connection("default")
        try:
            concurrente.set_autocommit(False)
            with concurrente.cursor() as cursor:
                cursor.execute(
                    "UPDATE organisme_agent SET role = %s, date_revocation = NULL"
                    " WHERE id = %s",
                    [AgentOrganismeRole.SUPERVISEUR.value, str(liaison.id)],
                )
            rattachement = executor.submit(attach)
            assert _a_lock_waiter_appears()
            concurrente.commit()
        finally:
            concurrente.rollback()
            concurrente.close()

        with pytest.raises(AgentDejaRattache):
            rattachement.result(timeout=10)

    liaison.refresh_from_db()
    assert liaison.role == AgentOrganismeRole.SUPERVISEUR.value
    assert liaison.date_revocation is None
    assert not AuditLogModel.objects.exists()
