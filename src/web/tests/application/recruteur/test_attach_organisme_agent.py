from uuid import uuid4

import pytest

from application.recruteur.usecases.attach_organisme_agent import (
    AttachOrganismeAgentCommand,
    AttachOrganismeAgentUsecase,
)
from config.app_config import AppConfig
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.organisme_agent_errors import AgentDejaRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="usecase")
def usecase_fixture(
    recruteur_integration_container,
) -> AttachOrganismeAgentUsecase:
    return recruteur_integration_container.attach_organisme_agent_usecase()


def test_responsable_attaches_bare_agent(db, usecase):
    responsable, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    bare_agent = AgentFactory.create_model()

    agent_organisme = usecase.execute(
        AttachOrganismeAgentCommand(
            organisme_id=organisme.id,
            agent_id=bare_agent.utilisateur_id,
            role=AgentOrganismeRole.MEMBRE,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=responsable.utilisateur_id, is_staff=False
            ),
        )
    )

    assert agent_organisme.entity_id == bare_agent.utilisateur_id
    assert agent_organisme.organisme_id == organisme.id
    assert agent_organisme.nom == bare_agent.utilisateur.last_name
    assert agent_organisme.prenom == bare_agent.utilisateur.first_name
    assert agent_organisme.email == bare_agent.utilisateur.email
    assert agent_organisme.poste == bare_agent.intitule_poste
    assert agent_organisme.role == AgentOrganismeRole.MEMBRE.value
    assert OrganismeAgentModel.objects.filter(
        organisme_id=organisme.id, agent_id=bare_agent.utilisateur_id
    ).exists()


def test_staff_bypasses_role_check(db, usecase):
    organisme = OrganismeFactory.create_model()
    bare_agent = AgentFactory.create_model()

    agent_organisme = usecase.execute(
        AttachOrganismeAgentCommand(
            organisme_id=organisme.id,
            agent_id=bare_agent.utilisateur_id,
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=True
            ),
        )
    )

    assert agent_organisme.role == AgentOrganismeRole.RESPONSABLE.value
    assert OrganismeAgentModel.objects.filter(
        organisme_id=organisme.id, agent_id=bare_agent.utilisateur_id
    ).exists()


def test_membre_is_denied(db, usecase):
    membre, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE
    )
    bare_agent = AgentFactory.create_model()

    with pytest.raises(AccesOrganismeRefuse):
        usecase.execute(
            AttachOrganismeAgentCommand(
                organisme_id=organisme.id,
                agent_id=bare_agent.utilisateur_id,
                role=AgentOrganismeRole.MEMBRE,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=membre.utilisateur_id, is_staff=False
                ),
            )
        )

    assert not OrganismeAgentModel.objects.filter(
        organisme_id=organisme.id, agent_id=bare_agent.utilisateur_id
    ).exists()


def test_raises_when_agent_already_attached(db, usecase):
    responsable, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    autre_agent = OrganismeFactory.create_agent_in_organisme(
        organisme.id, role=AgentOrganismeRole.MEMBRE
    )

    with pytest.raises(AgentDejaRattache):
        usecase.execute(
            AttachOrganismeAgentCommand(
                organisme_id=organisme.id,
                agent_id=autre_agent.utilisateur_id,
                role=AgentOrganismeRole.RESPONSABLE,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=responsable.utilisateur_id, is_staff=False
                ),
            )
        )


def test_raises_when_agent_does_not_exist(db, usecase):
    # TODO: implement test when usecase also updated
    pass


def test_raises_when_organisme_does_not_exist(db, usecase):
    bare_agent = AgentFactory.create_model()

    with pytest.raises(OrganismeNexistePas):
        usecase.execute(
            AttachOrganismeAgentCommand(
                organisme_id=uuid4(),
                agent_id=bare_agent.utilisateur_id,
                role=AgentOrganismeRole.MEMBRE,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
            )
        )
