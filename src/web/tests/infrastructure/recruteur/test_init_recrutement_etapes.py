from unittest.mock import Mock, patch

import pytest
from django.db.models.deletion import ProtectedError

from application.recruteur.dtos.recrutement_request import (
    RecrutementRequest,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.recrutement_errors import SupressionEtapeImpossible
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.factories.candidate.candidature_factory import CandidatureFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(Mock(spec=AuditLogWriter))
    return container


@pytest.fixture
def setup_base(db):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    agent, organisme = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE, etapes=etapes
    )
    recrutement_model = RecrutementFactory.create_model(
        organisme_id=organisme.id,
        agent_id=agent.utilisateur.username,
        agent_role=AgentRecrutementRole.RESPONSABLE,
        etapes=etapes,
        persist_etapes=True,
    )
    return etapes, agent, recrutement_model


class TestInitRecrutementEtapes:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"organisme_role": AgentOrganismeRole.SUPERVISEUR},
            {
                "organisme_role": AgentOrganismeRole.MEMBRE,
                "agent_role": AgentRecrutementRole.RESPONSABLE,
            },
        ],
        ids=["superviseur_organisme", "responsable_recrutement"],
    )
    def test_init_recrutement_etapes(self, db, recruteur_integration_container, kwargs):
        # parametres par defaut = une seule etape en cours
        en_cours = EtapeRecrutementFactory.create_entity()
        etapes = EtapeRecrutementFactory.create_entity_batch(en_cours=(en_cours,))

        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=kwargs.get("organisme_role"), etapes=etapes
        )
        utilisateur = UtilisateurFactory.create_entity(
            entity_id=agent.utilisateur.username
        )

        recrutement_model = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_id=agent.utilisateur.username,
            agent_role=kwargs.get("agent_role"),
            persist_etapes=False,
        )
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        resultat = usecase.execute(
            RecrutementRequest(
                organisme_id=recrutement_model.organisme_id,
                recrutement_id=recrutement_model.offre_id,
                utilisateur=utilisateur,
            )
        )

        for etape_result, etape_expected in zip(resultat, etapes, strict=True):
            assert etape_result.entity_id != etape_expected.entity_id
            assert etape_result.nom == etape_expected.nom
            assert etape_result.categorie == etape_expected.categorie

    @pytest.mark.parametrize(
        "agent_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR],
    )
    def test_denied_agents(self, db, recruteur_integration_container, agent_role):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE, etapes=etapes
        )
        utilisateur = UtilisateurFactory.create_entity(
            entity_id=agent.utilisateur.username
        )
        recrutement_model = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_id=agent.utilisateur.username,
            agent_role=agent_role,
            etapes=etapes,
            persist_etapes=True,
        )
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        with pytest.raises(AccesRecrutementRefuse):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur=utilisateur,
                )
            )

    def test_agents_without_role(self, db, recruteur_integration_container, setup_base):
        _, _, recrutement_model = setup_base
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )

    def test_raise_when_etape_has_candidatures(
        self, db, recruteur_integration_container, setup_base
    ):
        etapes, agent, recrutement_model = setup_base
        etape_model = EtapeModel.objects.get(id=etapes[0].entity_id)
        CandidatureFactory.create_model(
            offre_id=recrutement_model.offre_id,
            etape=etape_model,
        )
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        with pytest.raises(SupressionEtapeImpossible):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur=UtilisateurFactory.create_entity(
                        entity_id=agent.utilisateur.username
                    ),
                )
            )

    def test_raise_integrity_error(
        self,
        db,
        recruteur_integration_container,
        setup_base,
    ):
        etapes, agent, recrutement_model = setup_base
        etape_model = EtapeModel.objects.get(id=etapes[0].entity_id)
        CandidatureFactory.create_model(
            offre_id=recrutement_model.offre_id,
            etape=etape_model,
        )

        repository = recruteur_integration_container.postgres_recrutement_repository()
        repository.save = Mock(side_effect=ProtectedError("msg", []))

        # Bypasser domain check to test rollback if db error
        with patch.object(EtapeRecrutement, "delete", return_value=None):
            usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

            ordre_etapes_avant = recrutement_model.ordre_etapes
            nb_etapes_avant = recrutement_model.etapes.count()

            with pytest.raises(ProtectedError):
                usecase.execute(
                    RecrutementRequest(
                        organisme_id=recrutement_model.organisme_id,
                        recrutement_id=recrutement_model.offre_id,
                        utilisateur=UtilisateurFactory.create_entity(
                            entity_id=agent.utilisateur.username
                        ),
                    )
                )

            # check rollback
            recrutement_model.refresh_from_db()
            assert recrutement_model.etapes.count() == nb_etapes_avant
            assert recrutement_model.ordre_etapes == ordre_etapes_avant
            assert CandidatureModel.objects.filter(etape=etape_model).exists()
