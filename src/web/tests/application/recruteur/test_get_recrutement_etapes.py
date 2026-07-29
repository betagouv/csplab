from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.usecases.get_recrutement_etapes import (
    GetRecrutementEtapesQuery,
    GetRecrutementEtapesUsecase,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    return repo


@pytest.fixture(name="organisme_permission_service")
def organisme_permission_service_fixture():
    return MagicMock(spec=OrganismePermissionService)


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_repository, organisme_permission_service):
    return GetRecrutementEtapesUsecase(
        organisme_repository=organisme_repository,
        organisme_permission_service=organisme_permission_service,
    )


class TestGetRecrutementEtapesUsecase:
    def test_returns_default_pipeline(
        self, organisme_repository, organisme_permission_service, usecase
    ):
        organisme_id = uuid4()
        recrutement_id = uuid4()
        utilisateur_id = uuid4()

        resultat = usecase.execute(
            GetRecrutementEtapesQuery(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
                utilisateur_id=utilisateur_id,
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
        organisme_permission_service.est_autorise.assert_called_once_with(
            action=OrganismeAction.GET_RECRUTEMENT_ETAPES,
            organisme_id=organisme_id,
            agent_id=utilisateur_id,
            recrutement_id=recrutement_id,
            est_staff=False,
        )
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_raises_when_organisme_not_found(self, organisme_repository, usecase):
        organisme_id = uuid4()
        organisme_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                GetRecrutementEtapesQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )

    def test_raises_when_not_authorized(
        self, organisme_repository, organisme_permission_service, usecase
    ):
        organisme_id = uuid4()
        organisme_permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementEtapesQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )
