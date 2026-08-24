from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.dtos.etape_data import EtapeData
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesCommand,
    UpdateRecrutementEtapesUsecase,
)
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory


@pytest.fixture(name="organisme_permission_service")
def organisme_permission_service_fixture():
    return MagicMock(spec=OrganismePermissionService)


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_permission_service):
    return UpdateRecrutementEtapesUsecase(
        organisme_permission_service=organisme_permission_service,
    )


class TestUpdateRecrutementEtapesUsecase:
    def test_echoes_etapes_back_unchanged(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        recrutement_id = uuid4()
        utilisateur = UtilisateurFactory.create_entity()
        etapes = [
            EtapeData(
                etape_uuid=uuid4(),
                nom="Réception des candidatures",
                categorie=CategorieEtapeRecrutement.ENTREE,
            ),
            EtapeData(
                etape_uuid=None,
                nom="Recrutement",
                categorie=CategorieEtapeRecrutement.ACCEPTE,
            ),
        ]

        resultat = usecase.execute(
            UpdateRecrutementEtapesCommand(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
                utilisateur=utilisateur,
                etapes=etapes,
            )
        )

        assert resultat == etapes
        organisme_permission_service.est_autorise.assert_called_once_with(
            action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
            organisme_id=organisme_id,
            utilisateur=utilisateur,
            recrutement_id=recrutement_id,
        )

    def test_empty_etapes_returns_empty_result(self, usecase):
        resultat = usecase.execute(
            UpdateRecrutementEtapesCommand(
                organisme_id=uuid4(),
                recrutement_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(),
                etapes=[],
            )
        )

        assert resultat == []

    def test_raises_when_not_authorized(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        organisme_permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                    etapes=[],
                )
            )
