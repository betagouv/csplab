from typing import List
from unittest.mock import Mock
from uuid import uuid4

import pytest

from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    RecrutementEtapeIncoherents,
)
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesCommand,
    UpdateRecrutementEtapesUsecase,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.errors.recrutement_errors import SupressionEtapeImpossible
from domain.recruteur.events.etape_events import (
    EtapeAjoutee,
    EtapeRenommee,
    EtapeReordonnee,
    EtapeSupprimee,
)
from domain.recruteur.events.recrutement_events import RecrutementEtapesMisesAJour
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import (
    EtapeData,
)
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory


@pytest.fixture(name="etapes")
def etapes_fixture():
    return EtapeRecrutementFactory.create_entity_batch()


@pytest.fixture(name="organisme_recruteur")
def organisme_recruteur_fixture():
    return OrganismeRecruteurFactory.create_entity()


@pytest.fixture(name="recrutement")
def recrutement_fixture(organisme_recruteur, etapes):
    recrutement = RecrutementFactory.create_entity(
        organisme_id=organisme_recruteur.entity_id,
        etapes=etapes,
    )
    return recrutement


@pytest.fixture(name="permission_service")
def permission_service_fixture():
    service = Mock(spec=OrganismePermissionService)
    service.est_autorise.return_value = AgentRecrutementRole.RESPONSABLE
    return service


@pytest.fixture(name="audit_log_writer")
def audit_log_writer_fixture():
    return Mock(spec=AuditLogWriter)


@pytest.fixture(name="recrutement_repository")
def recrutement_repository_fixture(recrutement):
    repo = Mock(spec=IRecrutementRepository)
    repo.get_by_id.return_value = recrutement
    return repo


@pytest.fixture(name="organisme_recruteur_repository")
def organisme_recruteur_repository_fixture(organisme_recruteur):
    repo = Mock(spec=IOrganismeRecruteurRepository)
    repo.get_by_id.return_value = organisme_recruteur
    return repo


NUMBER_CHANGES = 5


@pytest.fixture(name="etapes_data")
def etapes_data_fixture(
    recrutement,
) -> List[EtapeData]:
    # e3 deleted
    e0, e1, e2, _, e4, e5 = recrutement.etapes
    return [
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


@pytest.fixture(name="usecase")
def usecase_fixture(
    permission_service,
    recrutement_repository,
    organisme_recruteur_repository,
    audit_log_writer,
):
    return UpdateRecrutementEtapesUsecase(
        permission_service=permission_service,
        recrutement_repository=recrutement_repository,
        organisme_recruteur_repository=organisme_recruteur_repository,
        audit_log_writer=audit_log_writer,
    )


class TestUpdateRecrutementEtapesUsecase:
    def test_updated_pipeline(
        self,
        permission_service,
        audit_log_writer,
        organisme_recruteur,
        recrutement,
        etapes_data,
        usecase,
    ):

        utilisateur = UtilisateurFactory.create_entity()
        organisme_id = organisme_recruteur.entity_id
        recrutement_id = recrutement.entity_id
        resultat = usecase.execute(
            UpdateRecrutementEtapesCommand(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
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
        permission_service.est_autorise.assert_called_once_with(
            action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
            organisme_id=organisme_id,
            utilisateur=utilisateur,
            recrutement_id=recrutement_id,
        )
        audit_log_writer.drain_events.assert_called_once_with(
            utilisateur_id=utilisateur.entity_id, aggregate=recrutement
        )
        events = recrutement.read_events()

        assert len(events) == NUMBER_CHANGES
        assert any(isinstance(e, RecrutementEtapesMisesAJour) for e in events)
        assert any(isinstance(e, EtapeAjoutee) for e in events)
        assert any(isinstance(e, EtapeSupprimee) for e in events)
        assert any(isinstance(e, EtapeRenommee) for e in events)
        assert any(isinstance(e, EtapeReordonnee) for e in events)

    def test_update_recrutement_etapes_raises_when_organisme_introuvable(
        self, organisme_recruteur_repository, usecase
    ):
        organisme_recruteur_repository.get_by_id.side_effect = OrganismeNexistePas(
            "not found"
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=uuid4(),
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[],
                )
            )

    def test_raises_when_organisme_recrutement_mismatch(self, recrutement, usecase):

        with pytest.raises(OrganismeRecrutementIncoherents):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=uuid4(),
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[],
                )
            )

    def test_raises_when_recrutement_etape_mismatch(self, organisme_recruteur, usecase):
        organisme_id = organisme_recruteur.entity_id
        config_etape_inconnue = EtapeData(
            etape_uuid=uuid4(),
            nom="Étape fantôme",
            categorie=CategorieEtapeRecrutement.EN_COURS,
        )

        with pytest.raises(RecrutementEtapeIncoherents):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[config_etape_inconnue],
                )
            )

    def test_raises_when_not_authorized(
        self, permission_service, organisme_recruteur, recrutement, usecase
    ):
        permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_recruteur.entity_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_recruteur.entity_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[],
                )
            )

    def test_raise_when_etape_has_candidatures(
        self, organisme_recruteur, recrutement_repository, usecase
    ):
        organisme_id = organisme_recruteur.entity_id
        etapes = EtapeRecrutementFactory.create_entity_batch(
            candidatures=[uuid4(), uuid4()]
        )
        recrutement = RecrutementFactory.create_entity(
            organisme_id=organisme_id, etapes=etapes
        )
        recrutement_repository.get_by_id.return_value = recrutement

        events = recrutement.read_events()

        e0, e1, _, e3, e4, e5 = etapes
        etapes_data = [
            EtapeData(etape_uuid=e.entity_id, nom=e.nom, categorie=e.categorie)
            for e in [e0, e1, e3, e4, e5]
        ]

        with pytest.raises(SupressionEtapeImpossible):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=etapes_data,
                )
            )

        assert len(events) == 0

    def test_raise_when_wrong_configuration(
        self, organisme_recruteur, recrutement_repository, usecase
    ):
        organisme_id = organisme_recruteur.entity_id
        etapes = EtapeRecrutementFactory.create_entity_batch(
            candidatures=[uuid4(), uuid4()]
        )
        recrutement = RecrutementFactory.create_entity(
            organisme_id=organisme_id, etapes=etapes
        )
        recrutement_repository.get_by_id.return_value = recrutement

        events = recrutement.read_events()

        with pytest.raises(ConfigurationEtapesInvalide):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes_data=[],
                )
            )

            assert len(events) == 0
