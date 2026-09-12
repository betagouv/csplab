from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.dtos.recrutement_read_models import (
    EtapeDto,
    LocalisationDto,
    OrganismeRecruteurDto,
    RecrutementDetailReadModel,
)
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from application.recruteur.usecases.get_recrutement_detail import (
    GetRecrutementDetailQuery,
    GetRecrutementDetailUsecase,
)
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory


def _recrutement_detail_read_model() -> RecrutementDetailReadModel:
    return RecrutementDetailReadModel(
        offer_id=uuid4(),
        intitule="Chargé de mission numérique",
        archive=False,
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
        etapes=[EtapeDto(etape_uuid=uuid4(), nom="Réception", categorie="ENTREE")],
    )


@pytest.fixture(name="can_execute")
def can_execute_fixture(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(
        "application.recruteur.usecases.get_recrutement_detail.can_execute", mock
    )
    return mock


@pytest.fixture(name="recrutement_query_service")
def recrutement_query_service_fixture():
    return MagicMock(spec=IRecrutementQueryService)


@pytest.fixture(name="usecase")
def usecase_fixture(can_execute, recrutement_query_service):
    return GetRecrutementDetailUsecase(
        recrutement_query_service=recrutement_query_service,
    )


class TestGetRecrutementDetail:
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
        read_model = _recrutement_detail_read_model()
        recrutement_query_service.get_detail_by_recrutement.return_value = read_model

        utilisateur = UtilisateurFactory.create_entity()
        result = usecase.execute(
            GetRecrutementDetailQuery(
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
        recrutement_query_service.get_detail_by_recrutement.assert_called_once_with(
            organisme_id=organisme_id, recrutement_id=recrutement_id
        )

    def test_returns_none_for_unknown_recrutement(
        self,
        can_execute,
        recrutement_query_service,
        usecase,
    ):
        can_execute.return_value = AgentOrganismeRole.RESPONSABLE
        recrutement_query_service.get_detail_by_recrutement.return_value = None

        result = usecase.execute(
            GetRecrutementDetailQuery(
                organisme_id=uuid4(),
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
                GetRecrutementDetailQuery(
                    organisme_id=organisme_id,
                    recrutement_id=uuid4(),
                    utilisateur=UtilisateurFactory.create_entity(),
                )
            )
