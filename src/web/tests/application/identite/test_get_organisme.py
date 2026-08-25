from uuid import uuid4

import pytest

from application.identite.usecases.get_organisme import GetOrganismeCommand
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory


class TestGetOrganismeUsecase:
    def test_returns_organisme(self, get_organisme_usecase):
        organisme_id = uuid4()
        organisme = OrganismeFactory.create_entity(entity_id=organisme_id)
        get_organisme_usecase.organisme_repository.get_by_id.return_value = organisme
        utilisateur = UtilisateurFactory.create_entity()

        resultat = get_organisme_usecase.execute(
            GetOrganismeCommand(organisme_id=organisme_id, utilisateur=utilisateur)
        )

        assert resultat is organisme
        get_organisme_usecase.permission_service.est_autorise.assert_called_once_with(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme_id,
            utilisateur=utilisateur,
        )

    def test_raises_when_not_authorized(self, get_organisme_usecase):
        organisme_id = uuid4()
        get_organisme_usecase.permission_service.est_autorise.side_effect = (
            AccesOrganismeRefuse(organisme_id)
        )

        with pytest.raises(AccesOrganismeRefuse):
            get_organisme_usecase.execute(
                GetOrganismeCommand(
                    organisme_id=organisme_id,
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )
