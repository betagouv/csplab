from unittest.mock import Mock, patch

import pytest

from application.recruteur.services.initialize_recrutement_etapes import (
    initialize_recrutement_etapes,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
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
    recrutement = RecrutementDjangoFactory(organisme=organisme, etapes=etapes)
    recrutement.refresh_from_db()
    ordre_avant, updated_at_avant = recrutement.ordre_etapes, recrutement.updated_at
    etapes_avant = sorted(recrutement.etapes.values_list("id", flat=True))

    with pytest.raises(RuntimeError):
        initialize_recrutement_etapes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=agent.utilisateur,
        )

    recrutement.refresh_from_db()
    assert recrutement.ordre_etapes == ordre_avant
    assert recrutement.updated_at == updated_at_avant
    assert sorted(recrutement.etapes.values_list("id", flat=True)) == etapes_avant


def test_does_not_log_when_save_fails(db):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    agent, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR, etapes=etapes
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme, etapes=etapes)
    recrutement.refresh_from_db()
    ordre_avant = recrutement.ordre_etapes
    etapes_avant = sorted(recrutement.etapes.values_list("id", flat=True))

    with (
        patch.object(RecrutementModel, "save", side_effect=RuntimeError("save failed")),
        pytest.raises(RuntimeError),
    ):
        initialize_recrutement_etapes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=agent.utilisateur,
        )

    recrutement.refresh_from_db()
    assert recrutement.ordre_etapes == ordre_avant
    assert sorted(recrutement.etapes.values_list("id", flat=True)) == etapes_avant
    assert not AuditLogModel.objects.exists()
