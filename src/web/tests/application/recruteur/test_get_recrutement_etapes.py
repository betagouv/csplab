from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.usecases.get_recrutement_etapes import (
    GetRecrutementEtapesQuery,
    GetRecrutementEtapesUsecase,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    return repo


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_repository):
    return GetRecrutementEtapesUsecase(organisme_repository=organisme_repository)


class TestGetRecrutementEtapesUsecase:
    def test_returns_default_pipeline(self, organisme_repository, usecase):
        organisme_id = uuid4()

        resultat = usecase.execute(
            GetRecrutementEtapesQuery(
                organisme_id=organisme_id,
                recrutement_id=uuid4(),
                utilisateur_id=uuid4(),
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
