from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from django.db.models.deletion import ProtectedError

from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
)
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesCommand,
)
from config.app_config import AppConfig
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.recrutement_errors import SupressionEtapeImpossible
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData
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


NUMBER_CHANGES = 5


class TestUpdateRecrutementEtapes:
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
    def test_update_recrutement_etapes(
        self, db, recruteur_integration_container, kwargs
    ):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=kwargs.get("organisme_role")
        )
        utilisateur = UtilisateurFactory.create_entity(
            entity_id=agent.utilisateur.username
        )

        recrutement_model = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_id=agent.utilisateur.username,
            agent_role=kwargs.get("agent_role"),
            etapes=etapes,
            persist_etapes=True,
        )
        e0, e1, e2, _, e4, e5 = recrutement_model.etapes.all()  # type: ignore[attr-defined]

        CandidatureFactory.create_models_with_etapes(
            offre_id=recrutement_model.offre_id,
            etapes=[e0, e1, e2, e4, e5],  # type: ignore[attr-defined]
        )

        etapes_data = [
            EtapeData(
                etape_uuid=e0.id,
                nom="Candidatures reçues",
                categorie=e0.categorie,
            ),
            EtapeData(
                etape_uuid=None,
                nom="Sourcing",
                categorie=CategorieEtapeRecrutement.EN_COURS,  # added
            ),
            *[
                EtapeData(
                    etape_uuid=e.id,
                    nom=e.nom,
                    categorie=e.categorie,
                )
                for e in [e2, e1, e4, e5]
            ],
        ]

        usecase = recruteur_integration_container.update_recrutement_etapes_usecase()

        resultat = usecase.execute(
            UpdateRecrutementEtapesCommand(
                organisme_id=recrutement_model.organisme_id,
                recrutement_id=recrutement_model.offre_id,
                utilisateur=utilisateur,
                etapes_data=etapes_data,
            )
        )

        assert [e.nom for e in resultat] == [
            "Candidatures reçues",
            "Sourcing",
            "Entretien",
            "Présélection",
            "Refus",
            "Recrutement",
        ]

    @pytest.mark.parametrize(
        "agent_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR],
    )
    def test_denied_agents(self, db, recruteur_integration_container, agent_role):
        recrutement_model = RecrutementFactory.create_model(agent_role=agent_role)
        usecase = recruteur_integration_container.update_recrutement_etapes_usecase()

        with pytest.raises(AccesRecrutementRefuse):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur=UtilisateurFactory.create_entity(
                        entity_id=recrutement_model.agents_liaisons.get().agent_id
                    ),
                    etapes_data=[],
                )
            )

    def test_agents_without_role(self, db, recruteur_integration_container):
        recrutement_model = RecrutementFactory.create_model()
        usecase = recruteur_integration_container.update_recrutement_etapes_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[],
                )
            )

    def test_update_recrutement_etapes_raises_when_organisme_introuvable(
        self, db, recruteur_integration_container
    ):
        usecase = recruteur_integration_container.update_recrutement_etapes_usecase()

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=uuid4(),
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[],
                )
            )

    def test_raises_when_organisme_recrutement_mismatch(
        self, db, recruteur_integration_container
    ):
        other_organisme = OrganismeFactory.create_model(entity_id=uuid4())
        etapes = EtapeRecrutementFactory.create_entity_batch()
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE
        )
        utilisateur = UtilisateurFactory.create_entity(
            entity_id=agent.utilisateur.username
        )
        recrutement_model = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_id=agent.utilisateur.username,
            agent_role=AgentRecrutementRole.RESPONSABLE,
            etapes=etapes,
            persist_etapes=True,
        )
        usecase = recruteur_integration_container.update_recrutement_etapes_usecase()
        with pytest.raises(OrganismeRecrutementIncoherents):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=other_organisme.id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur=utilisateur,
                    etapes_data=[],
                )
            )

    def test_raise_when_etape_has_candidatures(
        self, db, recruteur_integration_container
    ):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE
        )
        utilisateur = UtilisateurFactory.create_entity(
            entity_id=agent.utilisateur.username
        )

        recrutement_model = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_id=agent.utilisateur.username,
            agent_role=AgentRecrutementRole.RESPONSABLE,
            etapes=etapes,
            persist_etapes=True,
        )

        CandidatureFactory.create_models_with_etapes(
            offre_id=recrutement_model.offre_id,
            etapes=recrutement_model.etapes.all(),  # type: ignore[attr-defined]
        )

        e0, e1, e2, _, e4, e5 = etapes
        etapes_data = [
            EtapeData(
                etape_uuid=e0.entity_id,
                nom="Candidatures reçues",
                categorie=e0.categorie,
            ),
            EtapeData(
                etape_uuid=None,
                nom="Sourcing",
                categorie=CategorieEtapeRecrutement.EN_COURS,  # added
            ),
            *[
                EtapeData(
                    etape_uuid=e.entity_id,
                    nom=e.nom,
                    categorie=e.categorie,
                )
                for e in [e2, e1, e4, e5]
            ],
        ]

        usecase = recruteur_integration_container.update_recrutement_etapes_usecase()

        with pytest.raises(SupressionEtapeImpossible):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme.id,
                    recrutement_id=recrutement_model.offre.id,
                    utilisateur=utilisateur,
                    etapes_data=etapes_data,
                )
            )

    def test_raise_integrity_error(
        self,
        db,
        recruteur_integration_container,
    ):
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
        etape_model = EtapeModel.objects.get(id=etapes[0].entity_id)
        CandidatureFactory.create_model(
            offre_id=recrutement_model.offre_id,
            etape=etape_model,
        )
        e0, e1, e2, _, e4, e5 = etapes
        etapes_data = [
            EtapeData(
                etape_uuid=e0.entity_id,
                nom="Candidatures reçues",
                categorie=e0.categorie,
            ),
            EtapeData(
                etape_uuid=None,
                nom="Sourcing",
                categorie=CategorieEtapeRecrutement.EN_COURS,  # added
            ),
            *[
                EtapeData(
                    etape_uuid=e.entity_id,
                    nom=e.nom,
                    categorie=e.categorie,
                )
                for e in [e2, e1, e4, e5]
            ],
        ]

        repository = recruteur_integration_container.postgres_recrutement_repository()
        repository.save = Mock(side_effect=ProtectedError("msg", []))

        # Bypass domain check to test rollback if db error
        with patch.object(EtapeRecrutement, "delete", return_value=None):
            usecase = (
                recruteur_integration_container.update_recrutement_etapes_usecase()
            )

            ordre_etapes_avant = recrutement_model.ordre_etapes
            nb_etapes_avant = recrutement_model.etapes.count()

            with pytest.raises(ProtectedError):
                usecase.execute(
                    UpdateRecrutementEtapesCommand(
                        organisme_id=recrutement_model.organisme_id,
                        recrutement_id=recrutement_model.offre_id,
                        utilisateur=UtilisateurFactory.create_entity(
                            entity_id=agent.utilisateur.username
                        ),
                        etapes_data=etapes_data,
                    )
                )

            # check rollback
            recrutement_model.refresh_from_db()
            assert recrutement_model.etapes.count() == nb_etapes_avant
            assert recrutement_model.ordre_etapes == ordre_etapes_avant
            assert CandidatureModel.objects.filter(etape=etape_model).exists()
