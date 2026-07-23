from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.dtos.recrutement_read_models import (
    CandidatDto,
    CandidatureKanbanDto,
    EtapeKanbanReadModel,
    LocalisationDto,
    OrganismeRecruteurDto,
    RecrutementKanbanReadModel,
)
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanQuery,
    GetRecrutementKanbanUsecase,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole


def _recrutement_kanban_read_model() -> RecrutementKanbanReadModel:
    return RecrutementKanbanReadModel(
        offer_id=uuid4(),
        intitule="Chargé de mission numérique",
        date_publication=datetime.now(tz=timezone.utc),
        localisation=LocalisationDto(
            zone_geographique="EU",
            pays="FRA",
            region="11",
            departement="75",
            localisation_label="Paris 8e arrondissement",
            latitude=48.8748,
            longitude=2.3070,
        ),
        organisme_recruteur=OrganismeRecruteurDto(
            nom="Mairie de Paris", siret="21750001600019"
        ),
        categorie_offre="A",
        etapes=[
            EtapeKanbanReadModel(
                etape_uuid=uuid4(),
                nom="Réception des candidatures",
                categorie="ENTREE",
                candidatures=[
                    CandidatureKanbanDto(
                        uuid=uuid4(),
                        date_soumission=datetime.now(tz=timezone.utc),
                        date_derniere_activite=datetime.now(tz=timezone.utc),
                        candidat=CandidatDto(
                            uuid=uuid4(), nom="Dupont", prenom="Alice"
                        ),
                    )
                ],
            )
        ],
    )


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock()
    return repo


@pytest.fixture(name="organisme_permission_service")
def organisme_permission_service_fixture():
    return MagicMock(spec=OrganismePermissionService)


@pytest.fixture(name="recrutement_query_service")
def recrutement_query_service_fixture():
    return MagicMock(spec=IRecrutementQueryService)


@pytest.fixture(name="usecase")
def usecase_fixture(
    organisme_repository, organisme_permission_service, recrutement_query_service
):
    return GetRecrutementKanbanUsecase(
        organisme_repository=organisme_repository,
        organisme_permission_service=organisme_permission_service,
        recrutement_query_service=recrutement_query_service,
    )


class TestGetRecrutementKanban:
    @pytest.mark.parametrize(
        "role",
        [
            pytest.param(AgentOrganismeRole.RESPONSABLE, id="responsable"),
            pytest.param(AgentOrganismeRole.MEMBRE, id="membre"),
        ],
    )
    def test_returns_detail_when_authorized(
        self,
        organisme_repository,
        organisme_permission_service,
        recrutement_query_service,
        usecase,
        role,
    ):
        organisme_permission_service.est_autorise.return_value = role
        organisme_id = uuid4()
        recrutement_id = uuid4()
        read_model = _recrutement_kanban_read_model()
        recrutement_query_service.get_kanban_by_recrutement.return_value = read_model

        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
                utilisateur_id=uuid4(),
            )
        )

        assert result == read_model
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)
        recrutement_query_service.get_kanban_by_recrutement.assert_called_once_with(
            organisme_id=organisme_id, recrutement_id=recrutement_id
        )

    def test_returns_none_for_unknown_recrutement(
        self,
        organisme_repository,
        organisme_permission_service,
        recrutement_query_service,
        usecase,
    ):
        organisme_permission_service.est_autorise.return_value = (
            AgentOrganismeRole.RESPONSABLE
        )
        organisme_id = uuid4()
        recrutement_query_service.get_kanban_by_recrutement.return_value = None

        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme_id,
                recrutement_id=uuid4(),
                utilisateur_id=uuid4(),
            )
        )

        assert result is None
        organisme_repository.get_by_id.assert_called_once_with(organisme_id)

    def test_raises_when_not_authorized(self, organisme_permission_service, usecase):
        organisme_id = uuid4()
        organisme_permission_service.est_autorise.side_effect = AccesOrganismeRefuse(
            organisme_id
        )

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )

    def test_raises_when_organisme_not_found(
        self, organisme_repository, organisme_permission_service, usecase
    ):
        organisme_permission_service.est_autorise.return_value = (
            AgentOrganismeRole.RESPONSABLE
        )
        organisme_id = uuid4()
        organisme_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )
