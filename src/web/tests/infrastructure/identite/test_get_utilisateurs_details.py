import pytest
from faker import Faker

from config.app_config import AppConfig
from domain.identite.errors.identite_errors import UtilisateurNexistePas
from domain.identite.value_objects.organisme_role import OrganismeRole
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.candidat_factory import CandidatFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
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
    [CandidatFactory.create_model, AgentFactory.create_model],
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
    agent, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    if has_candidate_profile:
        CandidatFactory.create_model(username=agent.utilisateur.username)

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
    agent, organisme = OrganismeFactory.create_model_with_agent(
        nom=fake.word(), role=AgentOrganismeRole.MEMBRE
    )
    other_organisme = OrganismeFactory.create_model(
        nom=fake.word(),
        agent_id=agent.utilisateur_id,
        role=AgentOrganismeRole.RESPONSABLE,
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
