import pytest

from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurQuery,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from application.recruteur.usecases.update_organisme_steps import (
    EtapeData,
    UpdateOrganismeStepsCommand,
)
from config.app_config import AppConfig
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.identite.organisme_factory import OrganismeFactory
from tests.factories.recruteur.organisme_factory import (
    make_etapes_recrutement,
)

NB_ETAPES_PAR_DEFAUT = 6


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_get_organisme_steps(recruteur_integration_container):
    organisme_model = OrganismeFactory.create_model()
    organisme_model.save()
    usecase = recruteur_integration_container.get_organisme_recruteur_usecase()

    organisme = usecase.execute(command=GetOrganismeRecruteurQuery(organisme_model.id))
    events = organisme.collect_events()
    assert len(events) == 0
    assert organisme.entity_id == organisme_model.id


def test_initialize_organisme_steps(recruteur_integration_container):
    organisme_model = OrganismeFactory.create_model()
    usecase = recruteur_integration_container.initialize_organisme_steps_usecase()

    organisme = usecase.execute(
        command=InitializeOrganismeStepsCommand(organisme_id=organisme_model.id)
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert organisme.etapes is not None
    assert len(organisme.etapes) == NB_ETAPES_PAR_DEFAUT


def test_update_organisme_steps(recruteur_integration_container):
    etapes = make_etapes_recrutement()

    organisme_model = OrganismeFactory.create_model(etapes=etapes)

    nouvelles_etapes = [
        EtapeData(
            etape_uuid=etapes[0].entity_id,
            nom="Candidatures reçues",
            categorie=CategorieEtapeRecrutement.ENTREE,
        ),
        EtapeData(
            etape_uuid=None,
            nom="Entretien RH",
            categorie=CategorieEtapeRecrutement.EN_COURS,
        ),
        EtapeData(
            etape_uuid=etapes[-2].entity_id,
            nom="Refus",
            categorie=CategorieEtapeRecrutement.REFUS,
        ),
        EtapeData(
            etape_uuid=etapes[-1].entity_id,
            nom="Recrutement",
            categorie=CategorieEtapeRecrutement.ACCEPTE,
        ),
    ]

    usecase = recruteur_integration_container.update_organisme_steps_usecase()
    organisme = usecase.execute(
        command=UpdateOrganismeStepsCommand(
            organisme_id=organisme_model.id,
            etapes=nouvelles_etapes,
        )
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert events[0].event_name == "OrganismeEtapesMisesAJour"
    assert organisme.etapes is not None
    assert len(organisme.etapes) == len(nouvelles_etapes)
