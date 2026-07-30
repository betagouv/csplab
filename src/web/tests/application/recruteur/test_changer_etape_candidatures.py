from unittest.mock import Mock
from uuid import uuid4

import pytest

from application.recruteur.usecases.changer_etape_candidatures import (
    CandidatureAChanger,
    ChangerEtapeCandidaturesCommand,
    ChangerEtapeCandidaturesUsecase,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)


@pytest.fixture(name="organisme_recruteur_repository")
def organisme_recruteur_repository_fixture():
    repo = Mock(spec=IOrganismeRecruteurRepository)
    repo.get_by_id.return_value = Mock()
    return repo


@pytest.fixture(name="usecase")
def usecase_fixture(organisme_recruteur_repository):
    return ChangerEtapeCandidaturesUsecase(
        organisme_recruteur_repository=organisme_recruteur_repository
    )


class TestChangerEtapeCandidaturesUsecase:
    # TODO : failed updates are not yet tested, waiting for their implementation
    def test_echoes_all_candidatures_as_reussites(
        self, organisme_recruteur_repository, usecase
    ):
        organisme_id = uuid4()
        candidature_ids = [uuid4(), uuid4()]
        command = ChangerEtapeCandidaturesCommand(
            organisme_id=organisme_id,
            recrutement_id=uuid4(),
            etape_cible_id=uuid4(),
            candidatures=[
                CandidatureAChanger(candidature_id=cid, etape_actuelle_id=uuid4())
                for cid in candidature_ids
            ],
        )

        resultat = usecase.execute(command)

        assert resultat.reussites == candidature_ids
        assert resultat.echecs == []
        organisme_recruteur_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_empty_batch_returns_empty_result(self, usecase):
        command = ChangerEtapeCandidaturesCommand(
            organisme_id=uuid4(),
            recrutement_id=uuid4(),
            etape_cible_id=uuid4(),
            candidatures=[],
        )

        resultat = usecase.execute(command)

        assert resultat.reussites == []
        assert resultat.echecs == []

    def test_raises_when_organisme_not_found(
        self, organisme_recruteur_repository, usecase
    ):
        organisme_id = uuid4()
        organisme_recruteur_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    etape_cible_id=uuid4(),
                    candidatures=[
                        CandidatureAChanger(
                            candidature_id=uuid4(), etape_actuelle_id=uuid4()
                        )
                    ],
                )
            )
