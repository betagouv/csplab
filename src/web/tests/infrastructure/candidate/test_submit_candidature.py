import pytest
from faker import Faker

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from config.app_config import AppConfig
from domain.candidate.exceptions.candidature_errors import CandidatureDejaSoumise
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.utils.shared_fixtures import (
    create_shared_qdrant_repository,
)

fake = Faker()


@pytest.fixture
def candidate_container():
    shared_qdrant_repository = create_shared_qdrant_repository()

    container = CandidateContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    shared_container.vector_repository.override(shared_qdrant_repository)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(candidate_container):
    return candidate_container.app_config()


def test_submit_candidature_success(db, candidate_container):
    offre_id = fake.uuid4(cast_to=None)
    candidat_id = fake.uuid4(cast_to=None)
    command = SubmitApplicationCommand(offre_id=offre_id, candidat_id=candidat_id)

    usecase = candidate_container.submit_application_usecase()
    candidature = usecase.execute(command)

    assert candidature.statut == StatutCandidature.SOUMISE
    assert candidature.offre_id == offre_id
    assert candidature.candidat_id == candidat_id
    assert candidature.soumise_le is not None


def test_submit_candidature_failure(db, candidate_container):
    existing = CandidatureFactory.build_model(statut=StatutCandidature.SOUMISE)

    command = SubmitApplicationCommand(
        offre_id=existing.offre_id,
        candidat_id=existing.candidat_id,
    )

    usecase = candidate_container.submit_application_usecase()

    with pytest.raises(CandidatureDejaSoumise):
        usecase.execute(command)
