from unittest.mock import Mock, patch

import pytest
from faker import Faker

from application.identite.services.create_agent import create_agent
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)

fake = Faker("fr_FR")


@pytest.fixture(name="superviseur_et_organisme")
def superviseur_et_organisme_fixture(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    return agent.utilisateur, organisme


@patch.object(
    ProfilAgentModel,
    "save",
    new=Mock(side_effect=RuntimeError("profile write failed")),
)
def test_rolls_back_user_when_profile_write_fails(superviseur_et_organisme):
    superviseur, organisme = superviseur_et_organisme
    email = fake.email()

    with pytest.raises(RuntimeError):
        create_agent(email=email, organisme_id=organisme.id, utilisateur=superviseur)

    assert not UserModel.objects.filter(email=email).exists()
    assert not AuditLogModel.objects.exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_user_and_profile_when_audit_log_write_fails(
    superviseur_et_organisme,
):
    superviseur, organisme = superviseur_et_organisme
    email = fake.email()

    with pytest.raises(RuntimeError):
        create_agent(email=email, organisme_id=organisme.id, utilisateur=superviseur)

    assert not UserModel.objects.filter(email=email).exists()
    assert not ProfilAgentModel.objects.filter(utilisateur__email=email).exists()
