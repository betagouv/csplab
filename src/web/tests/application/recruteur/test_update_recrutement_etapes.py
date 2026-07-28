from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.dtos.etape_data import EtapeData
from application.recruteur.usecases.update_recrutement_etapes import (
    UpdateRecrutementEtapesCommand,
    UpdateRecrutementEtapesUsecase,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    return repo


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_repository):
    return UpdateRecrutementEtapesUsecase(organisme_repository=organisme_repository)


class TestUpdateRecrutementEtapesUsecase:
    def test_echoes_etapes_back_unchanged(self, organisme_repository, usecase):
        organisme_id = uuid4()
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
                recrutement_id=uuid4(),
                utilisateur_id=uuid4(),
                etapes=etapes,
            )
        )

        assert resultat == etapes
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_empty_etapes_returns_empty_result(self, usecase):
        resultat = usecase.execute(
            UpdateRecrutementEtapesCommand(
                organisme_id=uuid4(),
                recrutement_id=uuid4(),
                utilisateur_id=uuid4(),
                etapes=[],
            )
        )

        assert resultat == []

    def test_raises_when_organisme_not_found(self, organisme_repository, usecase):
        organisme_id = uuid4()
        organisme_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                UpdateRecrutementEtapesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                    etapes=[],
                )
            )
