from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.dtos.recrutement_read_models import (
    CandidatDto,
    CandidatureKanbanDto,
    EtapeKanbanReadModel,
    RecrutementKanbanReadModel,
)
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanQuery,
    GetRecrutementKanbanUsecase,
)
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory


def _recrutement_kanban_read_model() -> RecrutementKanbanReadModel:
    return RecrutementKanbanReadModel(
        offer_id=uuid4(),
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


@pytest.fixture(name="can_execute")
def can_execute_fixture(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(
        "application.recruteur.usecases.get_recrutement_kanban.can_execute", mock
    )
    return mock


@pytest.fixture(name="recrutement_query_service")
def recrutement_query_service_fixture():
    return MagicMock(spec=IRecrutementQueryService)


@pytest.fixture(name="usecase")
def usecase_fixture(can_execute, recrutement_query_service):
    return GetRecrutementKanbanUsecase(
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
        can_execute,
        recrutement_query_service,
        usecase,
        role,
    ):
        can_execute.return_value = role
        organisme_id = uuid4()
        recrutement_id = uuid4()
        read_model = _recrutement_kanban_read_model()
        recrutement_query_service.get_kanban_by_recrutement.return_value = read_model

        utilisateur = UtilisateurFactory.create_entity()
        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme_id,
                recrutement_id=recrutement_id,
                utilisateur=utilisateur,
            )
        )

        assert result == read_model
        can_execute.assert_called_once_with(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=organisme_id,
            utilisateur=utilisateur,
            recrutement_id=recrutement_id,
        )
        recrutement_query_service.get_kanban_by_recrutement.assert_called_once_with(
            organisme_id=organisme_id, recrutement_id=recrutement_id
        )

    def test_returns_none_for_unknown_recrutement(
        self,
        can_execute,
        recrutement_query_service,
        usecase,
    ):
        can_execute.return_value = AgentOrganismeRole.RESPONSABLE
        organisme_id = uuid4()
        recrutement_query_service.get_kanban_by_recrutement.return_value = None

        result = usecase.execute(
            GetRecrutementKanbanQuery(
                organisme_id=organisme_id,
                recrutement_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(),
            )
        )

        assert result is None

    def test_raises_when_not_authorized(self, can_execute, usecase):
        organisme_id = uuid4()
        can_execute.side_effect = AccesOrganismeRefuse(organisme_id)

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )
