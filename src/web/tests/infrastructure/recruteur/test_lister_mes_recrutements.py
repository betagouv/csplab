import pytest

from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsQuery,
)
from config.app_config import AppConfig
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
)
from domain.recruteur.value_objects.statut_recrutement import (
    StatutRecrutement,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.factories.candidate.candidature_factory import CandidatureFactory
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
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
    return recruteur_integration_container.lister_mes_recrutements_usecase()


class TestListerMesRecrutements:
    def _create_agent_responsable(self):
        agent = AgentFactory.create_model()
        organisme = OrganismeFactory.create_model(
            agent_id=agent.utilisateur_id, role=AgentOrganismeRole.RESPONSABLE
        )
        return agent.utilisateur_id, organisme

    def _lister_recrutements(self, usecase, organisme, agent_id, statut):
        return usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme.id,
                statut=statut,
                utilisateur_id=agent_id,
            )
        )

    def test_lister_actifs(self, usecase):
        agent_id, organisme = self._create_agent_responsable()
        recrutement_actif = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_ids=(agent_id,),
            etapes=EtapeRecrutementFactory.create_entities(),
        )
        RecrutementFactory.create_model(
            offre_archivee=True,
            organisme_id=organisme.id,
            agent_ids=(agent_id,),
        )
        etape_entree = EtapeModel.objects.filter(
            recrutement_id=recrutement_actif.offre_id,
            categorie=CategorieEtapeRecrutement.ENTREE.value,
        ).first()
        etape_en_cours = EtapeModel.objects.filter(
            recrutement_id=recrutement_actif.offre_id,
            categorie=CategorieEtapeRecrutement.EN_COURS.value,
        ).first()

        CandidatureFactory.create_model(
            offre_id=recrutement_actif.offre_id, etape=etape_entree
        )
        CandidatureFactory.create_model(
            offre_id=recrutement_actif.offre_id, etape=etape_en_cours
        )

        result = self._lister_recrutements(
            usecase, organisme, agent_id, StatutRecrutement.ACTIF
        )

        items = list(result.slice(0, 10))
        assert len(items) == 1
        assert items[0].offer_id == recrutement_actif.offre_id
        assert len(items[0].agents) == 1
        assert items[0].agents[0].nom != ""
        assert items[0].candidatures.total == 2  # noqa
        assert items[0].candidatures.a_traiter == 1
        assert items[0].candidatures.en_cours == 1

    def test_lister_archives(self, usecase):
        agent_id, organisme = self._create_agent_responsable()
        RecrutementFactory.create_model(organisme_id=organisme.id)
        recrutement_archive = RecrutementFactory.create_model(
            offre_archivee=True,
            organisme_id=organisme.id,
        )
        etape_accepte = EtapeModel.objects.filter(
            recrutement_id=recrutement_archive.offre_id,
            categorie=CategorieEtapeRecrutement.ACCEPTE.value,
        ).first()

        CandidatureFactory.create_model(
            offre_id=recrutement_archive.offre_id, etape=etape_accepte
        )

        result = self._lister_recrutements(
            usecase, organisme, agent_id, StatutRecrutement.ARCHIVE
        )

        items = list(result.slice(0, 10))
        assert len(items) == 1
        assert items[0].offer_id == recrutement_archive.offre_id
        assert items[0].finalise is True
        assert items[0].recrute is not None
        assert items[0].recrute != ""
