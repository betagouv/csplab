import pytest
from faker import Faker

from config.app_config import AppConfig
from domain.identite.errors.identite_errors import UtilisateurNexistePas
from domain.identite.value_objects.organisme_role import OrganismeRole
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.gateways.shared.logger import LoggerService

fake = Faker()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_get_unknown_uuid(db, identite_integration_container):
    usecase = identite_integration_container.get_utilisateur_details_usecase()

    with pytest.raises(UtilisateurNexistePas):
        usecase.execute(str(fake.uuid4()))


@pytest.mark.parametrize(
    "create_user_profile",
    [CandidatDjangoFactory, AgentDjangoFactory],
    ids=["candidat", "agent_without_role"],
)
def test_user_without_organisme_role_has_no_organisme_roles(
    db, identite_integration_container, create_user_profile
):
    user_profile = create_user_profile()
    usecase = identite_integration_container.get_utilisateur_details_usecase()

    result = usecase.execute(user_profile.utilisateur.username)

    assert result.organisme_roles == []


@pytest.mark.parametrize("has_candidate_profile", [True, False])
def test_agent_with_role_has_organisme_roles(
    db, identite_integration_container, has_candidate_profile
):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.RESPONSABLE)
    if has_candidate_profile:
        CandidatDjangoFactory(utilisateur=agent.utilisateur)

    usecase = identite_integration_container.get_utilisateur_details_usecase()

    result = usecase.execute(agent.utilisateur.username)

    assert result.organisme_roles == [
        OrganismeRole(
            organisme_uuid=organisme.id,
            nom=organisme.nom,
            role=AgentOrganismeRole.RESPONSABLE.value,
        )
    ]


def test_agent_with_multiple_roles(db, identite_integration_container):
    agent, organisme = create_organisme_with_agent(
        nom=fake.word(), role=AgentOrganismeRole.MEMBRE
    )
    other_organisme = OrganismeDjangoFactory(nom=fake.word())
    OrganismeAgentDjangoFactory(
        organisme=other_organisme,
        agent=agent,
        role=AgentOrganismeRole.RESPONSABLE.value,
    )
    usecase = identite_integration_container.get_utilisateur_details_usecase()

    result = usecase.execute(agent.utilisateur.username)

    assert result.organisme_roles == [
        OrganismeRole(
            organisme_uuid=organisme.id,
            nom=organisme.nom,
            role=AgentOrganismeRole.MEMBRE.value,
        ),
        OrganismeRole(
            organisme_uuid=other_organisme.id,
            nom=other_organisme.nom,
            role=AgentOrganismeRole.RESPONSABLE.value,
        ),
    ]
