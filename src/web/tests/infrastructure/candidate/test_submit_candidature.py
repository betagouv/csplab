from uuid import UUID, uuid4

import pytest
from django.db import IntegrityError
from faker import Faker
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from config.app_config import AppConfig
from domain.candidate.entities.candidature import Candidature
from domain.candidate.exceptions.candidature_errors import CandidatureDejaSoumise
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from infrastructure.di.candidate.candidate_container import CandidateContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.referentiel.offer_factory import OfferFactory
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
    offre = OfferFactory.create_model()
    candidate = CandidatFactory.create_model()

    command = SubmitApplicationCommand(
        offre_id=offre.to_entity().id, candidat_id=candidate.to_entity().entity_id
    )

    usecase = candidate_container.submit_application_usecase()
    candidature = usecase.execute(command)

    assert candidature.statut == StatutCandidature.SOUMISE
    assert candidature.offre_id == offre.to_entity().id
    assert candidature.candidat_id == candidate.to_entity().entity_id
    assert candidature.soumise_le is not None


def test_candidature_already_exists(db, candidate_container):
    offre = OfferFactory.create_model()
    candidate = CandidatFactory.create_model()
    offre_id = offre.to_entity().id
    candidate_id = candidate.to_entity().entity_id
    existing = CandidatureFactory.build_model(
        statut=StatutCandidature.SOUMISE, offre_id=offre_id, candidat_id=candidate_id
    )
    assert str(existing) == str(existing.id)

    command = SubmitApplicationCommand(
        offre_id=existing.offre.id,
        candidat_id=existing.candidat.utilisateur_id,
    )

    usecase = candidate_container.submit_application_usecase()

    with pytest.raises(CandidatureDejaSoumise):
        usecase.execute(command)


def test_candidate_does_not_exist(db, candidate_container):
    offre = OfferFactory.create_model()
    offre_id = offre.to_entity().id
    candidate_id = fake.uuid4(cast_to=None)

    command = SubmitApplicationCommand(
        offre_id=offre_id,
        candidat_id=candidate_id,
    )
    usecase = candidate_container.submit_application_usecase()

    with pytest.raises(CandidatInexistant):
        usecase.execute(command)


def test_offer_does_not_exist(db, candidate_container):
    offre_id = fake.uuid4(cast_to=None)
    candidate = CandidatFactory.create_model()
    candidate_id = candidate.to_entity().entity_id

    command = SubmitApplicationCommand(
        offre_id=offre_id,
        candidat_id=candidate_id,
    )
    usecase = candidate_container.submit_application_usecase()

    with pytest.raises(OfferDoesNotExist):
        usecase.execute(command)


# The following 3 tests call repo.save() directly (bypassing the validator)
# and verify the FK safety net in PostgresCandidatureRepository.
# transactional_db: autocommit so FK constraints are enforced immediately.
def test_save_raises_candidat_inexistant_on_fk_violation(
    transactional_db, candidate_container
):
    offre = OfferFactory.create_model()
    repo = candidate_container.candidature_repository()

    candidature = Candidature.build(
        entity_id=uuid4(),
        candidat_id=uuid4(),  # unknown candidat → FK violation on candidat_id
        offre_id=offre.id,
        statut=StatutCandidature.INITIAL,
        documents=None,
        soumise_le=None,
        mise_a_jour_le=None,
    )
    with pytest.raises(CandidatInexistant):
        repo.save(candidature)


def test_save_raises_offer_does_not_exist_on_fk_violation(
    transactional_db, candidate_container
):
    profil = CandidatFactory.create_model()
    repo = candidate_container.candidature_repository()

    candidature = Candidature.build(
        entity_id=uuid4(),
        candidat_id=UUID(profil.utilisateur_id),  # type: ignore[attr-defined]
        offre_id=uuid4(),  # unknown offer → FK violation on offre_id
        statut=StatutCandidature.INITIAL,
        documents=None,
        soumise_le=None,
        mise_a_jour_le=None,
    )
    with pytest.raises(OfferDoesNotExist):
        repo.save(candidature)


# transactional_db: FK + PK constraints enforced immediately
# (autocommit, production parity).
def test_save_raises_unhandled_integrity_error(transactional_db, candidate_container):
    profil1 = CandidatFactory.create_model()
    profil2 = CandidatFactory.create_model()
    offre1 = OfferFactory.create_model()
    offre2 = OfferFactory.create_model()

    shared_id = uuid4()
    repo = candidate_container.candidature_repository()

    c1 = Candidature.build(
        entity_id=shared_id,
        candidat_id=UUID(profil1.utilisateur_id),  # type: ignore[attr-defined]
        offre_id=offre1.id,
        statut=StatutCandidature.INITIAL,
        documents=None,
        soumise_le=None,
        mise_a_jour_le=None,
    )
    repo.save(c1)

    # Same entity_id → duplicate PK → error message contains "candidature_pkey",
    # not "candidat_id" nor "offre_id" → bare raise
    c2 = Candidature.build(
        entity_id=shared_id,
        candidat_id=UUID(profil2.utilisateur_id),  # type: ignore[attr-defined]
        offre_id=offre2.id,
        statut=StatutCandidature.INITIAL,
        documents=None,
        soumise_le=None,
        mise_a_jour_le=None,
    )
    with pytest.raises(IntegrityError):
        repo.save(c2)
