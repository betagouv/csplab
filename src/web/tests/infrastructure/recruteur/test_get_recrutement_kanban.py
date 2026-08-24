from uuid import uuid4

import pytest

from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanQuery,
)
from config.app_config import AppConfig
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.factories.candidate.candidature_factory import CandidatureFactory
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="usecase")
def usecase_fixture(recruteur_integration_container):
    return recruteur_integration_container.get_recrutement_kanban_usecase()


class TestGetRecrutementKanbanRbac:
    @pytest.mark.parametrize(
        ("role", "assign_agent_to_recrutement"),
        [
            pytest.param(AgentOrganismeRole.RESPONSABLE, False, id="responsable"),
            pytest.param(AgentOrganismeRole.MEMBRE, True, id="membre_assigned"),
        ],
    )
    def test_authorized(self, usecase, role, assign_agent_to_recrutement):
        agent, organisme = OrganismeFactory.create_model_with_agent(role=role)
        agent_id = agent.utilisateur_id if assign_agent_to_recrutement else None
        recrutement = RecrutementFactory.create_model(
            organisme_id=organisme.id, agent_id=agent_id
        )
        etape_entree = EtapeModel.objects.get(
            recrutement_id=recrutement.offre_id,
            categorie=CategorieEtapeRecrutement.ENTREE.value,
        )
        candidature = CandidatureFactory.create_model(
            offre_id=recrutement.offre_id, etape=etape_entree
        )

        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme.id,
                recrutement_id=recrutement.offre_id,
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result is not None
        assert result.offer_id == recrutement.offre_id
        assert len(result.etapes) == 6  # noqa
        assert result.etapes[0].categorie == "ENTREE"
        assert result.etapes[0].candidatures[0].uuid == candidature.id
        assert result.etapes[-1].categorie == "ACCEPTE"
        assert result.etapes[-1].candidatures == []

    def test_forbidden_when_membre_not_assigned_to_recrutement(self, usecase):
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE
        )
        recrutement = RecrutementFactory.create_model(organisme_id=organisme.id)

        with pytest.raises(AccesRecrutementRefuse):
            usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme.id,
                    recrutement_id=recrutement.offre_id,
                    utilisateur_id=agent.utilisateur_id,
                )
            )

    @pytest.mark.parametrize("est_staff", [False, True])
    def test_forbidden_when_agent_has_no_organisme_role(self, usecase, est_staff):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme.id,
                    recrutement_id=uuid4(),
                    utilisateur_id=agent.utilisateur_id,
                    est_staff=est_staff,
                )
            )

    def test_returns_none_for_unknown_recrutement(self, usecase):
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )

        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme.id,
                recrutement_id=uuid4(),
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result is None

    def test_returns_none_when_recrutement_belongs_to_another_organisme(self, usecase):
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )
        autre_organisme = OrganismeFactory.create_model()
        recrutement = RecrutementFactory.create_model(organisme_id=autre_organisme.id)

        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme.id,
                recrutement_id=recrutement.offre_id,
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result is None
