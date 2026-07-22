import pytest

from application.recruteur.usecases.get_recrutement_liste import (
    GetRecrutementListeQuery,
)
from application.recruteur.usecases.recrutement_detail_static_data import (
    STATIC_RECRUTEMENT_DETAIL,
)
from config.app_config import AppConfig
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="usecase")
def usecase_fixture(recruteur_integration_container):
    return recruteur_integration_container.get_recrutement_liste_usecase()


class TestGetRecrutementListeRbac:
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE]
    )
    def test_authorized_when_agent_has_organisme_role(self, usecase, role):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model(
            agent_id=agent.utilisateur_id, role=role
        )

        result = usecase.execute(
            GetRecrutementListeQuery(
                organisme_id=organisme.id,
                recrutement_id=STATIC_RECRUTEMENT_DETAIL["offer_id"],
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result == STATIC_RECRUTEMENT_DETAIL

    @pytest.mark.parametrize("est_staff", [False, True])
    def test_forbidden_when_agent_has_no_organisme_role(self, usecase, est_staff):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme.id,
                    recrutement_id=STATIC_RECRUTEMENT_DETAIL["offer_id"],
                    utilisateur_id=agent.utilisateur_id,
                    est_staff=est_staff,
                )
            )
