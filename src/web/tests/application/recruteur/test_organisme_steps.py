import pytest

from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurQuery,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsCommand,
)
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.events.etape_events import (
    EtapeAjoutee,
    EtapeReordonnee,
    EtapeSupprimee,
)
from domain.recruteur.events.organisme_recruteur_events import (
    OrganismeEtapesInitialises,
    OrganismeEtapesMisesAJour,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)


def test_get_organisme_steps(get_organisme_recruteur_usecase):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    get_organisme_recruteur_usecase.organisme_recruteur_repository.save(
        organisme_before
    )

    organisme = get_organisme_recruteur_usecase.execute(
        command=InitializeOrganismeStepsCommand(
            organisme_id=organisme_before.entity_id,
            utilisateur=UtilisateurFactory.create_entity(),
        )
    )

    events = organisme.collect_events()
    assert len(events) == 0
    assert organisme.entity_id == organisme_before.entity_id


def test_initialize_organisme_steps(initialize_organisme_steps_usecase):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    initialize_organisme_steps_usecase.organisme_recruteur_repository.save(
        organisme_before
    )

    organisme = initialize_organisme_steps_usecase.execute(
        command=InitializeOrganismeStepsCommand(
            organisme_id=organisme_before.entity_id,
            utilisateur=UtilisateurFactory.create_entity(),
        )
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert any(isinstance(e, OrganismeEtapesInitialises) for e in events)


NUMBER_CHANGES = 7


def test_update_organisme_steps(update_organisme_steps_usecase):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    organisme_before = OrganismeRecruteurFactory.create_entity(etapes=etapes)
    update_organisme_steps_usecase.organisme_recruteur_repository.save(organisme_before)
    utilisateur = UtilisateurFactory.create_entity()

    nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)

    organisme = update_organisme_steps_usecase.execute(
        command=UpdateOrganismeStepsCommand(
            utilisateur=utilisateur,
            organisme_id=organisme_before.entity_id,
            etapes=nouvelles_etapes,
        )
    )

    events = organisme.read_events()
    update_organisme_steps_usecase.audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=utilisateur.entity_id, aggregate=organisme
    )
    assert len(events) == NUMBER_CHANGES
    assert any(isinstance(e, OrganismeEtapesMisesAJour) for e in events)
    assert any(isinstance(e, EtapeAjoutee) for e in events)
    assert any(isinstance(e, EtapeSupprimee) for e in events)
    assert any(isinstance(e, EtapeReordonnee) for e in events)


def test_get_organisme_steps_raises_when_not_responsable(
    get_organisme_recruteur_usecase,
):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    get_organisme_recruteur_usecase.organisme_recruteur_repository.save(
        organisme_before
    )
    permission_service = get_organisme_recruteur_usecase.organisme_permission_service
    permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
        organisme_before.entity_id
    )

    with pytest.raises(AccesOrganismeRefuse):
        get_organisme_recruteur_usecase.execute(
            command=GetOrganismeRecruteurQuery(
                organisme_id=organisme_before.entity_id,
                utilisateur=UtilisateurFactory.create_entity(),
            )
        )


def test_initialize_organisme_steps_raises_when_not_responsable(
    initialize_organisme_steps_usecase,
):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    initialize_organisme_steps_usecase.organisme_recruteur_repository.save(
        organisme_before
    )
    permission_service = initialize_organisme_steps_usecase.organisme_permission_service
    permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
        organisme_before.entity_id
    )

    with pytest.raises(AccesOrganismeRefuse):
        initialize_organisme_steps_usecase.execute(
            command=InitializeOrganismeStepsCommand(
                organisme_id=organisme_before.entity_id,
                utilisateur=UtilisateurFactory.create_entity(),
            )
        )


def test_update_organisme_steps_raises_when_not_responsable(
    update_organisme_steps_usecase,
):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    organisme_before = OrganismeRecruteurFactory.create_entity(etapes=etapes)
    update_organisme_steps_usecase.organisme_recruteur_repository.save(organisme_before)
    permission_service = update_organisme_steps_usecase.organisme_permission_service
    permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
        organisme_before.entity_id
    )

    with pytest.raises(AccesOrganismeRefuse):
        update_organisme_steps_usecase.execute(
            command=UpdateOrganismeStepsCommand(
                utilisateur=UtilisateurFactory.create_entity(),
                organisme_id=organisme_before.entity_id,
                etapes=EtapeRecrutementFactory.to_etape_data_list(etapes),
            )
        )
