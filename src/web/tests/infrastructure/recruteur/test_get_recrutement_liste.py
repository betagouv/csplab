from uuid import UUID, uuid4

import pytest

from application.recruteur.usecases.get_recrutement_liste import (
    GetRecrutementListeQuery,
)
from config.app_config import AppConfig
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
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
        recrutement = RecrutementFactory.create_model(organisme_id=organisme.id)
        etape_entree = EtapeModel.objects.get(
            recrutement_id=recrutement.offre_id,
            categorie=CategorieEtapeRecrutement.ENTREE.value,
        )
        candidature = CandidatureFactory.create_model(
            offre_id=recrutement.offre_id, etape=etape_entree
        )

        result = usecase.execute(
            GetRecrutementListeQuery(
                organisme_id=organisme.id,
                recrutement_id=recrutement.offre_id,
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result is not None
        assert result.count() == 1
        items = list(result.slice(0, 10))
        item = items[0]
        assert item.uuid == UUID(candidature.id)
        assert item.candidat.uuid == UUID(candidature.candidat_id)
        assert item.etape.etape_uuid == etape_entree.id
        assert item.etape.categorie == "ENTREE"

    @pytest.mark.parametrize("est_staff", [False, True])
    def test_forbidden_when_agent_has_no_organisme_role(self, usecase, est_staff):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme.id,
                    recrutement_id=uuid4(),
                    utilisateur_id=agent.utilisateur_id,
                    est_staff=est_staff,
                )
            )

    def test_returns_none_for_unknown_recrutement(self, usecase):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model(
            agent_id=agent.utilisateur_id, role=AgentOrganismeRole.RESPONSABLE
        )

        result = usecase.execute(
            GetRecrutementListeQuery(
                organisme_id=organisme.id,
                recrutement_id=uuid4(),
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result is None

    def test_returns_none_when_recrutement_belongs_to_another_organisme(self, usecase):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model(
            agent_id=agent.utilisateur_id, role=AgentOrganismeRole.RESPONSABLE
        )
        autre_organisme = OrganismeFactory.create_model()
        recrutement = RecrutementFactory.create_model(organisme_id=autre_organisme.id)

        result = usecase.execute(
            GetRecrutementListeQuery(
                organisme_id=organisme.id,
                recrutement_id=recrutement.offre_id,
                utilisateur_id=agent.utilisateur_id,
            )
        )

        assert result is None
