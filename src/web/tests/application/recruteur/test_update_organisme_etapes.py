from unittest.mock import Mock, patch

import pytest

from application.recruteur.services.update_organisme_etapes import (
    update_organisme_etapes,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_when_audit_log_fails(db):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, etapes=etapes
    )
    organisme.refresh_from_db()
    etapes_avant, updated_at_avant = organisme.etapes, organisme.updated_at

    with pytest.raises(RuntimeError):
        update_organisme_etapes(
            organisme_id=organisme.id,
            utilisateur=agent.utilisateur,
            etapes=EtapeRecrutementFactory.to_etape_data_list(etapes),
        )

    organisme.refresh_from_db()
    assert organisme.etapes == etapes_avant
    assert organisme.updated_at == updated_at_avant


def test_does_not_log_when_save_fails(db):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, etapes=etapes
    )

    with (
        patch.object(OrganismeModel, "save", side_effect=RuntimeError("save failed")),
        pytest.raises(RuntimeError),
    ):
        update_organisme_etapes(
            organisme_id=organisme.id,
            utilisateur=agent.utilisateur,
            etapes=EtapeRecrutementFactory.to_etape_data_list(etapes),
        )

    assert not AuditLogModel.objects.exists()
