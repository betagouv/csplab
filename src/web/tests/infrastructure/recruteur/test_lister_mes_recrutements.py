from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsQuery,
)
from config.app_config import AppConfig
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
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
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    container.organisme_permission_service.override(
        MagicMock(spec=OrganismePermissionService)
    )
    return container


class TestListerMesRecrutements:
    def test_lister_actifs(self, recruteur_integration_container):
        usecase = recruteur_integration_container.lister_mes_recrutements_usecase()
        organisme = OrganismeFactory.create_model()
        offre_active = OfferFactory.create_model(archived_at=None)
        offre_archivee = OfferFactory.create_model(archived_at=datetime(2024, 1, 1))
        agent = AgentFactory.create_model()
        agent_id = UUID(agent.utilisateur_id)
        recrutement_actif = RecrutementFactory.create_model(
            offre_id=offre_active.id,
            organisme_id=organisme.id,
            agent_ids=(agent_id,),
            etapes=EtapeRecrutementFactory.create_entities(),
        )
        RecrutementFactory.create_model(
            offre_id=offre_archivee.id,
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

        CandidatureFactory.create_model(offre_id=offre_active.id, etape=etape_entree)
        CandidatureFactory.create_model(offre_id=offre_active.id, etape=etape_en_cours)

        result = usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme.id,
                statut=StatutRecrutement.ACTIF,
                utilisateur_id=uuid4(),
            )
        )

        items = list(result.slice(0, 10))
        assert len(items) == 1
        assert items[0].offer_id == offre_active.id
        assert len(items[0].agents) == 1
        assert items[0].agents[0].nom != ""
        assert items[0].candidatures.total == 2  # noqa
        assert items[0].candidatures.a_traiter == 1
        assert items[0].candidatures.en_cours == 1

    def test_lister_archives(self, recruteur_integration_container):
        usecase = recruteur_integration_container.lister_mes_recrutements_usecase()
        organisme = OrganismeFactory.create_model()
        offre_active = OfferFactory.create_model(archived_at=None)
        offre_archivee = OfferFactory.create_model(archived_at=datetime(2024, 1, 1))
        RecrutementFactory.create_model(
            offre_id=offre_active.id,
            organisme_id=organisme.id,
        )
        recrutement_archive = RecrutementFactory.create_model(
            offre_id=offre_archivee.id,
            organisme_id=organisme.id,
        )
        etape_accepte = EtapeModel.objects.filter(
            recrutement_id=recrutement_archive.offre_id,
            categorie=CategorieEtapeRecrutement.ACCEPTE.value,
        ).first()

        CandidatureFactory.create_model(offre_id=offre_archivee.id, etape=etape_accepte)

        result = usecase.execute(
            ListerMesRecrutementsQuery(
                organisme_id=organisme.id,
                statut=StatutRecrutement.ARCHIVE,
                utilisateur_id=uuid4(),
            )
        )

        items = list(result.slice(0, 10))
        assert len(items) == 1
        assert items[0].offer_id == offre_archivee.id
        assert items[0].finalise is True
        assert items[0].recrute is not None
        assert items[0].recrute != ""
