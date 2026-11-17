from unittest.mock import Mock, patch

import pytest

from application.recruteur.services.add_recrutement_agent_tag import (
    add_recrutement_agent_tag,
)
from application.recruteur.services.remove_recrutement_agent_tag import (
    remove_recrutement_agent_tag,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.tag.models import RecrutementAgentTagModel, TagCategory
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    RecrutementAgentTagDjangoFactory,
    TagDjangoFactory,
)


def _superviseur_et_membre():
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = RecrutementAgentDjangoFactory(recrutement__organisme=organisme)
    return superviseur, membre


# transactional_db : `db` masquerait un select_for_update hors transaction.atomic()
def test_add_recrutement_agent_tag_runs_in_its_own_transaction(transactional_db):
    superviseur, membre = _superviseur_et_membre()
    tag = TagDjangoFactory(
        organisme=membre.recrutement.organisme, category=TagCategory.RECRUTEMENT_AGENT
    )

    add_recrutement_agent_tag(
        organisme_id=membre.recrutement.organisme_id,
        recrutement_id=membre.recrutement_id,
        agent_id=membre.agent_id,
        tag_id=tag.id,
        utilisateur=superviseur.utilisateur,
    )

    assert list(
        RecrutementAgentTagModel.objects.filter(recrutement_agent=membre).values_list(
            "tag_id", flat=True
        )
    ) == [tag.id]


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_add_recrutement_agent_tag_rolls_back_when_audit_log_fails(db):
    superviseur, membre = _superviseur_et_membre()
    tag = TagDjangoFactory(
        organisme=membre.recrutement.organisme, category=TagCategory.RECRUTEMENT_AGENT
    )

    with pytest.raises(RuntimeError):
        add_recrutement_agent_tag(
            organisme_id=membre.recrutement.organisme_id,
            recrutement_id=membre.recrutement_id,
            agent_id=membre.agent_id,
            tag_id=tag.id,
            utilisateur=superviseur.utilisateur,
        )

    assert not RecrutementAgentTagModel.objects.filter(
        recrutement_agent=membre
    ).exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_remove_recrutement_agent_tag_rolls_back_when_audit_log_fails(db):
    superviseur, membre = _superviseur_et_membre()
    pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)

    with pytest.raises(RuntimeError):
        remove_recrutement_agent_tag(
            organisme_id=membre.recrutement.organisme_id,
            recrutement_id=membre.recrutement_id,
            agent_id=membre.agent_id,
            tag_id=pose.tag_id,
            utilisateur=superviseur.utilisateur,
        )

    assert RecrutementAgentTagModel.objects.filter(pk=pose.pk).exists()
