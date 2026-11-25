from unittest.mock import MagicMock

import pytest
from django.utils import timezone
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


def _data(
    external_id: str, siret: str, parent_external_id=None, referentiel="DILA"
) -> OrganismeUpsertData:
    return OrganismeUpsertData(
        nom=f"Service {external_id}",
        versant=Verse.FPE,
        siret=SIRET(code=siret),
        localisation=None,
        parent_external_id=parent_external_id,
        external_id=external_id,
        referentiel=referentiel,
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
    assert [error["error"] for error in result["errors"]] == [
        "parent_external_id parent inconnu dans le référentiel DILA"
    ]
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


def test_updating_an_organisme_keeps_its_id_and_rewrites_its_parent():
    parent = OrganismeDjangoFactory(referentiel="DILA", external_id="parent")
    child = OrganismeDjangoFactory(
        referentiel="DILA", external_id="child", parent_id=None
    )

    result = _upsert(_data("child", "11000101300017", parent_external_id="parent"))

    assert result["updated"] == 1
    assert _get("child").id == child.id
    assert _get("child").parent_id == parent.id


def test_deleted_parent_is_rejected():
    OrganismeDjangoFactory(
        referentiel="DILA", external_id="parent", supprime_le=timezone.now()
    )

    result = _upsert(_data("child", "11000101300017", parent_external_id="parent"))

    assert [error["error"] for error in result["errors"]] == [
        "parent_external_id parent inconnu dans le référentiel DILA"
    ]
    assert not OrganismeModel.objects.filter(external_id="child").exists()


def test_deleted_parent_sent_in_the_same_batch_is_rejected():
    OrganismeDjangoFactory(
        referentiel="DILA",
        external_id="parent",
        siret="11000007200014",
        supprime_le=timezone.now(),
    )

    result = _upsert(
        _data("parent", "11000007200014"),
        _data("child", "11000101300017", parent_external_id="parent"),
    )

    assert [error["error"] for error in result["errors"]] == [
        "parent_external_id parent inconnu dans le référentiel DILA"
    ]
    assert not OrganismeModel.objects.filter(external_id="child").exists()


def test_organisme_cannot_be_its_own_parent():
    result = _upsert(_data("child", "11000101300017", parent_external_id="child"))

    assert [error["error"] for error in result["errors"]] == [
        "parent_external_id child inconnu dans le référentiel DILA"
    ]
    assert not OrganismeModel.objects.filter(external_id="child").exists()


def test_children_of_a_parent_rejected_for_a_siret_conflict_are_rejected():
    OrganismeDjangoFactory(referentiel="DILA", siret="11000101300017")

    result = _upsert(
        _data("parent", "11000101300017", referentiel="FINESS"),
        _data("child", "11000007200014", "parent", referentiel="FINESS"),
        _data("grandchild", "13002526500013", "child", referentiel="FINESS"),
    )

    assert result["created"] == 0
    assert [error["error"] for error in result["errors"]][1:] == [
        "parent de FINESS child rejeté dans le même lot",
        "parent de FINESS grandchild rejeté dans le même lot",
    ]
    assert not OrganismeModel.objects.filter(referentiel="FINESS").exists()
