from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.usecases.get_recrutement_etapes import (
    GetRecrutementEtapesQuery,
    GetRecrutementEtapesUsecase,
)
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory


@pytest.fixture(name="organisme_permission_service")
def organisme_permission_service_fixture():
    return MagicMock(spec=OrganismePermissionService)


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_permission_service):
    return GetRecrutementEtapesUsecase(
        organisme_permission_service=organisme_permission_service,
    )


class TestGetRecrutementEtapesUsecase:
    def test_returns_default_pipeline(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        recrutement_id = uuid4()
        utilisateur = UtilisateurFactory.create_entity()

        resultat = usecase.execute(
            GetRecrutementEtapesQuery(
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
        organisme_permission_service.est_autorise.assert_called_once_with(
            action=OrganismeAction.GET_RECRUTEMENT_ETAPES,
            organisme_id=organisme_id,
            utilisateur=utilisateur,
            recrutement_id=recrutement_id,
        )

    def test_raises_when_not_authorized(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        organisme_permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementEtapesQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )
