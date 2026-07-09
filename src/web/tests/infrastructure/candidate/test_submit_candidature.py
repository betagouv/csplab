from datetime import datetime, timezone
from uuid import uuid4

import pytest
import time_machine
from faker import Faker

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from config.app_config import AppConfig
from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory
from tests.factories.referentiel.offer_factory import OfferFactory
from tests.utils.shared_fixtures import (
    create_shared_qdrant_repository,
)

fake = Faker()
_FROZEN_TS = datetime.now(tz=timezone.utc)


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


@time_machine.travel(_FROZEN_TS, tick=False)
def test_submit_candidature_success(db, candidate_container):
    offre = OfferFactory.create_model()
    candidate = CandidatFactory.create_model()

    RecrutementFactory.create_model(offre_id=offre.id)

    command = SubmitApplicationCommand(
        offre_id=offre.id,  # type: ignore[attr-defined]
        candidat_id=candidate.to_entity().entity_id,
    )

    usecase = candidate_container.submit_application_usecase()
    candidature = usecase.execute(command)

    assert candidature.statut == StatutCandidature.SOUMISE
    assert candidature.soumise_le == _FROZEN_TS


def test_candidate_does_not_exist(db, candidate_container):
    offre = OfferFactory.create_model()
    candidate_id = fake.uuid4(cast_to=None)

    command = SubmitApplicationCommand(
        offre_id=offre.id,  # type: ignore[attr-defined]
        candidat_id=candidate_id,
    )
    usecase = candidate_container.submit_application_usecase()

    with pytest.raises(CandidatInexistant):
        usecase.execute(command)


def test_recrutement_does_not_exist(db, candidate_container):
    offre_id = fake.uuid4(cast_to=None)
    candidate = CandidatFactory.create_model()
    candidate_id = candidate.to_entity().entity_id

    command = SubmitApplicationCommand(
        offre_id=offre_id,
        candidat_id=candidate_id,
    )
    usecase = candidate_container.submit_application_usecase()

    with pytest.raises(RecrutementInexistant):
        usecase.execute(command)


# The following tests call repo.save() directly and verify the FK safety net.
# transactional_db: autocommit so FK constraints are enforced immediately.
# We first create the row via the recruteur repo (which knows etape_id)
# and then verify the candidate repo catches FK violations.
def test_save_raises_candidat_inexistant_on_fk_violation(
    transactional_db, candidate_container
):
    offre = OfferFactory.create_model()
    recrutement = RecrutementFactory.create_model(offre_id=offre.id)

    # Now try to save with an unknown candidat_id via candidate repo
    candidature = Candidature.build(
        entity_id=uuid4(),
        candidat_id=uuid4(),  # unknown candidat
        offre_id=recrutement.offre_id,  # type: ignore[attr-defined]
        statut=StatutCandidature.INITIAL,
        documents=None,
        soumise_le=None,
        mise_a_jour_le=None,
    )
    with pytest.raises(CandidatInexistant):
        candidate_container.candidature_repository().save(candidature)
