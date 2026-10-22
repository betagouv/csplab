from unittest.mock import Mock, patch

import pytest
from django.db import IntegrityError

from application.recruteur.services.create_tag import create_tag
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.tag.models import TagCategory, TagModel, TagQuerySet
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
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


@patch.object(TagQuerySet, "create", side_effect=IntegrityError("other constraint"))
def test_does_not_translate_other_integrity_errors(mock_create, superviseur):
    agent, organisme = superviseur

    with pytest.raises(IntegrityError, match="other constraint"):
        create_tag(
            organisme_id=organisme.id,
            utilisateur=agent.utilisateur,
            name="Expert",
            category=TagCategory.CANDIDATURE,
        )
