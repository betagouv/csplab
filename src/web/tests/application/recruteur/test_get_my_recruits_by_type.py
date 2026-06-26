from uuid import uuid4

import pytest

from application.recruteur.dtos.my_recruits_dtos import (
    RecrutementActifDTO,
    RecrutementArchiveDTO,
)
from application.recruteur.errors import ErreurPaginationQuery
from application.recruteur.usecases.get_my_recruits_by_type import (
    GetMyRecruitsByTypeQuery,
)
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory
from tests.factories.referentiel.offer_factory import OfferFactory


class InMemoryPage:
    def __init__(self, items):
        self._items = items

    def count(self):
        return len(self._items)

    def slice(self, offset, limit):
        return iter(self._items[offset : offset + limit])


def test_query_raises_if_incorrect_values():
    with pytest.raises(ErreurPaginationQuery):
        GetMyRecruitsByTypeQuery(
            organisme_id=uuid4(),
            recrutement_status=RecrutementStatus.ACTIF,
            size=0,
        )
    with pytest.raises(ErreurPaginationQuery):
        GetMyRecruitsByTypeQuery(
            organisme_id=uuid4(),
            recrutement_status=RecrutementStatus.ACTIF,
            page=0,
        )


def test_get_my_recruits_by_type_actifs(get_my_recruits_by_type_usecase):
    organisme_id = uuid4()
    agent = AgentFactory.create_entity()
    offers = OfferFactory.create_entity_batch(10)
    recrutements = RecrutementFactory.create_entity_batch(
        offers, responsables_ids=[agent.entity_id]
    )

    get_my_recruits_by_type_usecase.offers_repository.upsert_batch(offers)
    get_my_recruits_by_type_usecase.agents_repository.get_by_ids = lambda ids: [agent]

    get_my_recruits_by_type_usecase.recrutements_repository.filter_by_status = (
        lambda *_: InMemoryPage(recrutements)
    )

    result = get_my_recruits_by_type_usecase.execute(
        GetMyRecruitsByTypeQuery(
            organisme_id=organisme_id,
            recrutement_status=RecrutementStatus.ACTIF,
            page=2,
            size=2,
        )
    )

    assert result.total == 10  # noqa
    assert len(result.items) == 2  # noqa
    item = result.items[0]
    assert isinstance(item, RecrutementActifDTO)
    assert item.offer_id == offers[2].id
    assert item.intitule == offers[2].title
    assert len(item.responsables) == 1
    assert item.responsables[0].nom == f"{agent.prenom} {agent.nom}"


def test_get_my_recruits_by_type_archives_avec_candidat(
    get_my_recruits_by_type_usecase,
):
    organisme_id = uuid4()
    candidat = CandidatFactory.create_entity()
    offers = OfferFactory.create_entity_batch(10)
    recrutements = RecrutementFactory.create_entity_batch(
        offers,
        organisme_id=organisme_id,
        status=RecrutementStatus.ARCHIVE,
        candidat_recrute_id=candidat.entity_id,
    )

    get_my_recruits_by_type_usecase.offers_repository.upsert_batch(offers)
    get_my_recruits_by_type_usecase.candidat_repository.get_by_ids = lambda ids: [
        candidat
    ]
    get_my_recruits_by_type_usecase.recrutements_repository.filter_by_status = (
        lambda *_: InMemoryPage(recrutements)
    )

    result = get_my_recruits_by_type_usecase.execute(
        GetMyRecruitsByTypeQuery(
            organisme_id=organisme_id,
            recrutement_status=RecrutementStatus.ARCHIVE,
            page=2,
            size=2,
        )
    )

    assert result.total == 10  # noqa
    assert len(result.items) == 2  # noqa
    item = result.items[0]
    assert isinstance(item, RecrutementArchiveDTO)
    assert item.finalise is True
    assert item.recrute == f"{candidat.prenom} {candidat.nom}"


def test_get_my_recruits_by_type_archives_sans_candidat(
    get_my_recruits_by_type_usecase,
):
    organisme_id = uuid4()
    offers = OfferFactory.create_entity_batch(10)
    recrutements = RecrutementFactory.create_entity_batch(
        offers,
        organisme_id=organisme_id,
        status=RecrutementStatus.ARCHIVE,
        candidat_recrute_id=None,
    )

    get_my_recruits_by_type_usecase.offers_repository.upsert_batch(offers)
    get_my_recruits_by_type_usecase.recrutements_repository.filter_by_status = (
        lambda *_: InMemoryPage(recrutements)
    )

    result = get_my_recruits_by_type_usecase.execute(
        GetMyRecruitsByTypeQuery(
            organisme_id=organisme_id,
            recrutement_status=RecrutementStatus.ARCHIVE,
            page=2,
            size=2,
        )
    )

    assert result.total == 10  # noqa
    assert len(result.items) == 2  # noqa
    item = result.items[0]
    assert isinstance(item, RecrutementArchiveDTO)
    assert item.finalise is False
    assert item.recrute is None
