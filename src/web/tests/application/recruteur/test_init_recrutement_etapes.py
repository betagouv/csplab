from unittest.mock import Mock
from uuid import uuid4

import pytest

from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    OrganismeRecruteurSansEtapes,
)
from application.recruteur.usecases.init_recrutement_etapes import (
    InitRecrutementEtapesUsecase,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import SupressionEtapeImpossible
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
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


@pytest.fixture(name="organisme_recruteur")
def organisme_recruteur_fixture():
    etapes = EtapeRecrutementFactory.create_entity_batch()
    return OrganismeRecruteurFactory.create_entity(etapes)


@pytest.fixture(name="recrutement")
def recrutement_fixture(organisme_recruteur):
    recrutement = RecrutementFactory.create_entity(
        organisme_id=organisme_recruteur.entity_id
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


@pytest.fixture(name="usecase")
def usecase_fixture(
    permission_service,
    recrutement_repository,
    organisme_recruteur_repository,
    audit_log_writer,
):
    return InitRecrutementEtapesUsecase(
        permission_service=permission_service,
        recrutement_repository=recrutement_repository,
        organisme_recruteur_repository=organisme_recruteur_repository,
        audit_log_writer=audit_log_writer,
    )


class TestInitRecrutementEtapesUsecase:
    def test_returns_default_pipeline(
        self,
        permission_service,
        audit_log_writer,
        organisme_recruteur,
        recrutement,
        usecase,
    ):

        utilisateur = UtilisateurFactory.create_entity()
        organisme_id = organisme_recruteur.entity_id
        recrutement_id = recrutement.entity_id
        resultat = usecase.execute(
            RecrutementRequest(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
                utilisateur=utilisateur,
            )
        )

        assert [e.nom for e in resultat] == [
            "Réception des candidatures",
            "Présélection",
            "Entretien",
            "Proposition",
            "Refus",
            "Recrutement",
        ]
        permission_service.est_autorise.assert_called_once_with(
            action=OrganismeAction.INIT_RECRUTEMENT_ETAPES,
            organisme_id=organisme_id,
            utilisateur=utilisateur,
            recrutement_id=recrutement_id,
        )
        audit_log_writer.drain_events.assert_called_once_with(
            utilisateur_id=utilisateur.entity_id, aggregate=recrutement
        )
        events = recrutement.collect_events()

        assert len(events) == 1 + len(organisme_recruteur.etapes) + len(
            recrutement.etapes
        )

    def test_raises_when_organisme_not_found(
        self, organisme_recruteur_repository, recrutement, usecase
    ):
        organisme_id = uuid4()

        organisme_recruteur_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )

    def test_raises_when_organisme_has_no_etapes(
        self, organisme_recruteur_repository, recrutement, usecase
    ):
        organisme_no_etapes = OrganismeRecruteurFactory.create_entity()
        organisme_recruteur_repository.get_by_id.return_value = organisme_no_etapes

        with pytest.raises(OrganismeRecruteurSansEtapes):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=uuid4(),
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )

    def test_raises_when_organisme_recrutement_mismatch(self, recrutement, usecase):
        organisme_id = uuid4()

        with pytest.raises(OrganismeRecrutementIncoherents):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
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
                RecrutementRequest(
                    organisme_id=organisme_recruteur.entity_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
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

        events = recrutement.collect_events()

        with pytest.raises(SupressionEtapeImpossible):
            usecase.execute(
                RecrutementRequest(
                    organisme_id=organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )

        assert len(events) == 0
