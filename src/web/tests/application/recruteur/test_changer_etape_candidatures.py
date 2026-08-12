from unittest.mock import MagicMock, Mock
from uuid import uuid4

import pytest

from application.recruteur.usecases.changer_etape_candidatures import (
    ChangerEtapeCandidaturesCommand,
    ChangerEtapeCandidaturesUsecase,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesRecrutementRefuse
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementEtapeInexistante,
    RecrutementInexistant,
)
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.changement_etape_candidatures import (
    ChangementEtapeCandidaturesResultat,
)
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.factories.recruteur.candidature_recruteur_factory import (
    CandidatureRecruteurFactory,
)
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory


@pytest.fixture(name="organisme_recruteur_repository")
def organisme_recruteur_repository_fixture():
    repo = Mock(spec=IOrganismeRecruteurRepository)
    repo.get_by_id.return_value = Mock()
    return repo


@pytest.fixture(name="recrutement")
def recrutement_fixture():
    recrutement = RecrutementFactory.create_entity()
    return recrutement


@pytest.fixture(name="recrutement_repository")
def recrutement_repository_fixture(recrutement):
    repo = Mock(spec=IRecrutementRepository)
    repo.get_by_id.return_value = recrutement
    return repo


@pytest.fixture(name="candidatures_recruteur")
def candidatures_recruteur_fixture(recrutement):
    return CandidatureRecruteurFactory.create_entities(
        3,
        recrutement_id=recrutement.entity_id,
    )


@pytest.fixture(name="candidatures_recruteur_changees")
def candidatures_recruteur_changees_fixture(candidatures_recruteur, recrutement):
    return [
        c.changer_etape(etape_id=recrutement.etapes[-1]) for c in candidatures_recruteur
    ]


@pytest.fixture(name="candidature_recruteur_repository")
def candidature_recruteur_repository_fixture(
    candidatures_recruteur, candidatures_recruteur_changees
):
    repo = Mock(spec=ICandidatureRecruteurRepository)
    repo.get_by_ids.return_value = candidatures_recruteur
    repo.upsert.return_value = ChangementEtapeCandidaturesResultat(
        reussites=candidatures_recruteur_changees, echecs=[]
    )

    return repo


@pytest.fixture(name="permission_service")
def permission_service_fixture():
    service = MagicMock(spec=OrganismePermissionService)
    service.est_autorise.return_value = AgentRecrutementRole.RESPONSABLE
    return service


@pytest.fixture(name="usecase")
def usecase_fixture(
    organisme_recruteur_repository,
    recrutement_repository,
    candidature_recruteur_repository,
    permission_service,
):
    return ChangerEtapeCandidaturesUsecase(
        organisme_recruteur_repository=organisme_recruteur_repository,
        candidature_recruteur_repository=candidature_recruteur_repository,
        recrutement_repository=recrutement_repository,
        permission_service=permission_service,
    )


class TestChangerEtapeCandidaturesUsecase:
    def test_echoes_all_candidatures_as_reussites(
        self,
        recrutement,
        candidatures_recruteur,
        candidatures_recruteur_changees,
        usecase,
    ):
        command = ChangerEtapeCandidaturesCommand(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.entity_id,
            utilisateur_id=uuid4(),
            est_staff=False,
            etape_cible_id=recrutement.etapes[-1].entity_id,
            candidatures=[
                candidature.entity_id for candidature in candidatures_recruteur
            ],
        )

        resultat = usecase.execute(command)

        assert resultat.reussites == candidatures_recruteur_changees
        assert resultat.echecs == []

    def test_raises_when_recrutement_not_found(
        self, recrutement_repository, candidatures_recruteur, usecase
    ):
        recrutement_id = uuid4()
        recrutement_repository.get_by_id.side_effect = RecrutementInexistant(
            recrutement_id
        )

        with pytest.raises(RecrutementInexistant):
            usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=uuid4(),
                    recrutement_id=recrutement_id,
                    utilisateur_id=uuid4(),
                    est_staff=False,
                    etape_cible_id=uuid4(),
                    candidatures=[c.entity_id for c in candidatures_recruteur],
                )
            )

    def test_raises_when_unauthorized(
        self, permission_service, recrutement, candidatures_recruteur, usecase
    ):
        permission_service.est_autorise.side_effect = AccesRecrutementRefuse(
            recrutement.entity_id
        )

        with pytest.raises(
            AccesRecrutementRefuse,
            match=f"Rôle non autorisé sur le recrutement {recrutement.entity_id}",
        ):
            usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=recrutement.organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur_id=uuid4(),
                    est_staff=False,
                    etape_cible_id=recrutement.etapes[1].entity_id,
                    candidatures=[c.entity_id for c in candidatures_recruteur],
                )
            )

    def test_raises_when_recrutement_id_does_not_belong_to_organisme(
        self, recrutement, candidatures_recruteur, permission_service, usecase
    ):
        organisme_id = uuid4()
        permission_service.est_autorise.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )
        with pytest.raises(
            OrganismeNexistePas,
            match=(f"Organisme introuvable : {organisme_id}"),
        ):
            usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur_id=uuid4(),
                    est_staff=False,
                    etape_cible_id=recrutement.etapes[1].entity_id,
                    candidatures=[c.entity_id for c in candidatures_recruteur],
                )
            )

    def test_raises_when_target_etape_does_not_belong_to_recrutement(
        self, recrutement, candidatures_recruteur, usecase
    ):
        etape_cible_id = uuid4()

        with pytest.raises(
            RecrutementEtapeInexistante,
            match=f"Etape {etape_cible_id} inexistante pour ce recrutement"
            f" {recrutement.entity_id}",
        ):
            usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=recrutement.organisme_id,
                    recrutement_id=recrutement.entity_id,
                    utilisateur_id=uuid4(),
                    est_staff=False,
                    etape_cible_id=etape_cible_id,
                    candidatures=[c.entity_id for c in candidatures_recruteur],
                )
            )

    def test_return_results_with_domain_errors(
        self, recrutement, candidature_recruteur_repository, usecase
    ):
        candidatures = CandidatureRecruteurFactory.create_entities(
            3, recrutement_id=uuid4()
        )
        candidature_recruteur_repository.get_by_ids.return_value = candidatures
        candidature_recruteur_repository.upsert.return_value = (
            ChangementEtapeCandidaturesResultat(reussites=[], echecs=[])
        )
        result = usecase.execute(
            ChangerEtapeCandidaturesCommand(
                organisme_id=recrutement.organisme_id,
                recrutement_id=recrutement.entity_id,
                utilisateur_id=uuid4(),
                est_staff=False,
                etape_cible_id=recrutement.etapes[1].entity_id,
                candidatures=[c.entity_id for c in candidatures],
            )
        )
        assert result.reussites == []
        assert result.echecs == [
            (
                candidature.entity_id,
                RecrutementCandidatureInexistante(
                    candidature_id=candidature.entity_id,
                    recrutement_id=recrutement.entity_id,
                ).message,
            )
            for candidature in candidatures
        ]
