from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from faker import Faker

from application.recruteur.usecases.changer_etape_candidatures import (
    CandidatureAChanger,
    ChangerEtapeCandidaturesCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.candidate.candidature_factory import CandidatureFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.gateways.shared.logger import LoggerService

fake = Faker("fr_FR")


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(MagicMock(spec=AuditLogWriter))
    return container


class TestChangerEtapeCandidatures:
    # TODO : update this class after persistence is implemented
    def test_changer_etape_candidatures(self, db, recruteur_integration_container):
        organisme_model = OrganismeFactory.create_model()
        candidature_model = CandidatureFactory.create_model()
        etape_cible_id = uuid4()
        usecase = recruteur_integration_container.changer_etape_candidatures_usecase()

        resultat = usecase.execute(
            command=ChangerEtapeCandidaturesCommand(
                organisme_id=organisme_model.id,
                recrutement_id=candidature_model.etape.recrutement_id,
                etape_cible_id=etape_cible_id,
                candidatures=[
                    CandidatureAChanger(
                        candidature_id=candidature_model.id,
                        etape_actuelle_id=candidature_model.etape_id,
                    )
                ],
            )
        )

        assert resultat.reussites == [candidature_model.id]
        assert resultat.echecs == []

    def test_changer_etape_candidatures_raises_when_organisme_introuvable(
        self, db, recruteur_integration_container
    ):
        candidature_model = CandidatureFactory.create_model()
        usecase = recruteur_integration_container.changer_etape_candidatures_usecase()

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                command=ChangerEtapeCandidaturesCommand(
                    organisme_id=uuid4(),
                    recrutement_id=candidature_model.etape.recrutement_id,
                    etape_cible_id=uuid4(),
                    candidatures=[
                        CandidatureAChanger(
                            candidature_id=candidature_model.id,
                            etape_actuelle_id=candidature_model.etape_id,
                        )
                    ],
                )
            )
