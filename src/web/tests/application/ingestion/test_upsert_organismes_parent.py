from unittest.mock import MagicMock

import pytest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.upsert_organismes_input import (
    OrganismeUpsertData,
    UpsertOrganismesInput,
)
from application.ingestion.usecases.upsert_organismes import UpsertOrganismesUsecase
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)

pytestmark = pytest.mark.django_db


def _data(external_id: str, siret: str, parent_external_id=None) -> OrganismeUpsertData:
    return OrganismeUpsertData(
        nom=f"Service {external_id}",
        versant=Verse.FPE,
        siret=SIRET(code=siret),
        localisation=None,
        parent_external_id=parent_external_id,
        external_id=external_id,
        referentiel="DILA",
        millesime="2026-11-25",
    )


def _upsert(*data: OrganismeUpsertData):
    usecase = UpsertOrganismesUsecase(
        organisme_repository=PostgresOrganismeRepository(), logger=MagicMock()
    )
    return usecase.execute(UpsertOrganismesInput(organismes=list(data)))


def _get(external_id: str) -> OrganismeModel:
    return OrganismeModel.objects.get(referentiel="DILA", external_id=external_id)


def test_parent_is_resolved_from_an_existing_organisme():
    parent = OrganismeDjangoFactory(referentiel="DILA", external_id="parent")

    _upsert(_data("child", "11000101300017", parent_external_id="parent"))

    assert _get("child").parent_id == parent.id


def test_parent_is_resolved_when_sent_after_its_child_in_the_same_batch():
    result = _upsert(
        _data("child", "11000101300017", parent_external_id="parent"),
        _data("parent", "11000007200014"),
    )

    assert result["errors"] == []
    assert _get("child").parent_id == _get("parent").id


def test_parent_is_looked_up_in_the_same_referentiel():
    OrganismeDjangoFactory(referentiel="FINESS", external_id="parent")

    result = _upsert(_data("child", "11000101300017", parent_external_id="parent"))

    assert result["created"] == 0
    assert not OrganismeModel.objects.filter(external_id="child").exists()


def test_organisme_with_an_unknown_parent_is_rejected_and_the_others_are_kept():
    result = _upsert(
        _data("child", "11000101300017", parent_external_id="ghost"),
        _data("other", "11000007200014"),
    )

    assert result["created"] == 1
    assert [error["error"] for error in result["errors"]] == [
        "parent_external_id ghost inconnu dans le référentiel DILA"
    ]
    assert not OrganismeModel.objects.filter(external_id="child").exists()
