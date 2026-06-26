import pytest

from application.recruteur.dtos.my_recruits_dtos import (
    RecrutementActifDTO,
    RecrutementArchiveDTO,
)
from application.recruteur.usecases.get_my_recruits_by_type import (
    GetMyRecruitsByTypeQuery,
)
from config.app_config import AppConfig
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.identite.organisme_factory import OrganismeFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory
from tests.factories.referentiel.offer_factory import OfferFactory


@pytest.fixture(name="recruteur_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_get_my_recruits_by_type_actifs(recruteur_container):
    # --- Seed DB ---
    organisme_model = OrganismeFactory.create_model()
    organisme_id = organisme_model.id

    agent_model = AgentFactory.create_model()
    agent_entity_id = agent_model.utilisateur_id  # type: ignore[attr-defined]

    offer_models = OfferFactory.create_model_batch(5)

    recrutement_repo = recruteur_container.postgres_recrutement_repository()
    for offer_model in offer_models:
        recrutement = RecrutementFactory.create_entity(
            offre_id=offer_model.id,
            organisme_id=organisme_id,
            responsables_ids=(agent_entity_id,),
            status=RecrutementStatus.ACTIF,
        )
        recrutement_repo.save(recrutement)

    # --- Execute ---
    usecase = recruteur_container.get_my_recruits_by_type_usecase()
    result = usecase.execute(
        GetMyRecruitsByTypeQuery(
            organisme_id=organisme_id,
            recrutement_status=RecrutementStatus.ACTIF,
            page=2,
            size=2,
        )
    )

    # --- Assert ---
    offer_ids = {o.id for o in offer_models}
    assert result.total == 5  # noqa
    assert len(result.items) == 2  # noqa
    item = result.items[0]
    assert isinstance(item, RecrutementActifDTO)
    assert item.offer_id in offer_ids
    assert len(item.responsables) == 1


def test_get_my_recruits_by_type_archives_avec_candidat(recruteur_container):
    # --- Seed DB ---
    organisme_model = OrganismeFactory.create_model()
    organisme_id = organisme_model.id

    candidat_model = CandidatFactory.create_model(prenom="Marie", nom="Martin")

    offer_models = OfferFactory.create_model_batch(5)

    recrutement_repo = recruteur_container.postgres_recrutement_repository()
    for offer_model in offer_models:
        recrutement = RecrutementFactory.create_entity(
            offre_id=offer_model.id,
            organisme_id=organisme_id,
            status=RecrutementStatus.ARCHIVE,
            candidat_recrute_id=candidat_model.utilisateur_id,  # type: ignore[attr-defined]
        )
        recrutement_repo.save(recrutement)

    # --- Execute ---
    usecase = recruteur_container.get_my_recruits_by_type_usecase()
    result = usecase.execute(
        GetMyRecruitsByTypeQuery(
            organisme_id=organisme_id,
            recrutement_status=RecrutementStatus.ARCHIVE,
            page=2,
            size=2,
        )
    )

    # --- Assert ---
    assert result.total == 5  # noqa
    assert len(result.items) == 2  # noqa
    item = result.items[0]
    assert isinstance(item, RecrutementArchiveDTO)
    assert item.finalise is True
    assert item.recrute == "Marie Martin"


def test_get_my_recruits_by_type_archives_sans_candidat(recruteur_container):
    # --- Seed DB ---
    organisme_model = OrganismeFactory.create_model()
    organisme_id = organisme_model.id

    offer_models = OfferFactory.create_model_batch(5)

    recrutement_repo = recruteur_container.postgres_recrutement_repository()
    for offer_model in offer_models:
        recrutement = RecrutementFactory.create_entity(
            offre_id=offer_model.id,
            organisme_id=organisme_id,
            status=RecrutementStatus.ARCHIVE,
            candidat_recrute_id=None,
        )
        recrutement_repo.save(recrutement)

    # --- Execute ---
    usecase = recruteur_container.get_my_recruits_by_type_usecase()
    result = usecase.execute(
        GetMyRecruitsByTypeQuery(
            organisme_id=organisme_id,
            recrutement_status=RecrutementStatus.ARCHIVE,
            page=2,
            size=2,
        )
    )

    # --- Assert ---
    assert result.total == 5  # noqa
    assert len(result.items) == 2  # noqa
    item = result.items[0]
    assert isinstance(item, RecrutementArchiveDTO)
    assert item.finalise is False
    assert item.recrute is None
