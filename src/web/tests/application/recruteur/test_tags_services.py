from unittest.mock import Mock, patch

import pytest

from application.recruteur.services.create_tag import create_tag
from application.recruteur.services.delete_tag import delete_tag
from application.recruteur.services.update_tag import update_tag
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.tag.models import (
    CandidatureTagModel,
    TagCategory,
    TagColor,
    TagModel,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    TagDjangoFactory,
)


@pytest.fixture(name="superviseur")
def superviseur_fixture(db):
    return create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_when_audit_log_fails(superviseur):
    agent, organisme = superviseur

    with pytest.raises(RuntimeError):
        create_tag(
            organisme_id=organisme.id,
            utilisateur=agent.utilisateur,
            name="Expert",
            category=TagCategory.CANDIDATURE,
        )

    assert not TagModel.objects.exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_update_rolls_back_when_audit_log_fails(superviseur):
    agent, organisme = superviseur
    tag = TagDjangoFactory(organisme=organisme, name="Expert")

    with pytest.raises(RuntimeError):
        update_tag(
            organisme_id=organisme.id,
            tag_id=tag.id,
            utilisateur=agent.utilisateur,
            name="Bon profil",
            color=TagColor.BLEU,
        )

    tag.refresh_from_db()
    assert tag.name == "Expert"


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_delete_rolls_back_when_audit_log_fails(superviseur):
    agent, organisme = superviseur
    tag = TagDjangoFactory(organisme=organisme)
    CandidatureTagDjangoFactory(tag=tag)

    with pytest.raises(RuntimeError):
        delete_tag(
            organisme_id=organisme.id, tag_id=tag.id, utilisateur=agent.utilisateur
        )

    assert TagModel.objects.filter(pk=tag.pk).exists()
    assert CandidatureTagModel.objects.filter(tag=tag).exists()
