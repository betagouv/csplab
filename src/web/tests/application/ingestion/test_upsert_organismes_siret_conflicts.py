from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from django.utils import timezone
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.upsert_organismes_input import (
    OrganismeUpsertData,
    UpsertOrganismesInput,
)
from application.ingestion.usecases.upsert_organismes import UpsertOrganismesUsecase
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.django_apps.tag.models import TagModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    TagDjangoFactory,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
    takes_precedence_over,
)

pytestmark = pytest.mark.django_db

SIRET_A = "11000101300017"
SIRET_B = "11000007200014"

VERSANT_BY_REFERENTIEL = {"DILA": Verse.FPE, "FINESS": Verse.FPH, "GIPCDG": Verse.FPT}


def _data(referentiel: str, external_id: str, **overrides) -> OrganismeUpsertData:
    fields = {
        "nom": f"Organisme {referentiel} {external_id}",
        "versant": VERSANT_BY_REFERENTIEL[referentiel],
        "siret": SIRET(code=SIRET_A),
        "localisation": None,
        "parent_id": None,
        "external_id": external_id,
        "referentiel": referentiel,
        "millesime": "2026-10-28",
        "entity_id": uuid4(),
    }
    fields.update(overrides)
    return OrganismeUpsertData(**fields)


def _upsert(*data: OrganismeUpsertData):
    usecase = UpsertOrganismesUsecase(
        organisme_repository=PostgresOrganismeRepository(), logger=MagicMock()
    )
    return usecase.execute(UpsertOrganismesInput(organismes=list(data)))


def _siret_holder(siret: str = SIRET_A) -> OrganismeModel:
    return OrganismeModel.objects.not_supprimes().get(siret=siret)


@pytest.mark.parametrize(
    "referentiel,other,expected",
    [
        ("DILA", "GIPCDG", True),
        ("DILA", "FINESS", True),
        ("FINESS", "GIPCDG", True),
        ("GIPCDG", "DILA", False),
        ("FINESS", "DILA", False),
        ("GIPCDG", "FINESS", False),
        ("DILA", "DILA", False),
        ("DILA", None, False),
        (None, "GIPCDG", False),
    ],
)
def test_takes_precedence_over(referentiel, other, expected):
    assert takes_precedence_over(referentiel, other) is expected


def test_dila_takes_the_siret_of_a_gipcdg_organisme():
    _upsert(_data("GIPCDG", "gip-1"))

    result = _upsert(_data("DILA", "dila-1", nom="Premier ministre"))

    assert result["created"] == 1
    assert result["errors"] == []
    holder = _siret_holder()
    assert (holder.referentiel, holder.nom) == ("DILA", "Premier ministre")
    assert not OrganismeModel.objects.filter(referentiel="GIPCDG").exists()


def test_gipcdg_reimport_after_dila_does_not_take_back_the_siret():
    _upsert(_data("GIPCDG", "gip-1"))
    _upsert(_data("DILA", "dila-1"))

    result = _upsert(_data("GIPCDG", "gip-1", nom="New name"))

    assert result["created"] == 0
    assert result["updated"] == 0
    assert len(result["errors"]) == 1
    assert SIRET_A in result["errors"][0]["error"]
    assert _siret_holder().referentiel == "DILA"
    assert not OrganismeModel.objects.filter(referentiel="GIPCDG").exists()


def test_gipcdg_imported_after_dila_is_rejected():
    _upsert(_data("DILA", "dila-1"))

    result = _upsert(_data("GIPCDG", "gip-1"))

    assert result["created"] == 0
    assert len(result["errors"]) == 1
    assert _siret_holder().referentiel == "DILA"
    assert not OrganismeModel.objects.filter(referentiel="GIPCDG").exists()


def test_finess_takes_the_siret_of_a_gipcdg_organisme():
    _upsert(_data("GIPCDG", "gip-1"))

    result = _upsert(_data("FINESS", "finess-1"))

    assert result["created"] == 1
    assert _siret_holder().referentiel == "FINESS"


def test_dila_takes_the_siret_of_a_finess_organisme():
    _upsert(_data("FINESS", "finess-1"))

    _upsert(_data("DILA", "dila-1"))

    assert _siret_holder().referentiel == "DILA"


def test_manually_created_organisme_keeps_its_siret():
    OrganismeDjangoFactory(siret=SIRET_A, referentiel=None)

    result = _upsert(_data("DILA", "dila-1"))

    assert result["created"] == 0
    assert len(result["errors"]) == 1
    assert _siret_holder().referentiel is None


def test_soft_deleted_organisme_is_replaced():
    OrganismeDjangoFactory(
        siret=SIRET_A, referentiel="GIPCDG", supprime_le=timezone.now()
    )

    result = _upsert(_data("DILA", "dila-1"))

    assert result["created"] == 1
    assert _siret_holder().referentiel == "DILA"


def test_dependents_are_moved_to_the_new_organisme():
    gipcdg = OrganismeDjangoFactory(siret=SIRET_A, referentiel="GIPCDG")
    agent_link = OrganismeAgentDjangoFactory(organisme=gipcdg)
    recrutement = RecrutementDjangoFactory(organisme=gipcdg)
    talentsoft = TalentsoftOrganismeDjangoFactory(organisme=gipcdg)
    child = OrganismeDjangoFactory(parent_id=gipcdg.id)
    tag = TagDjangoFactory(organisme=gipcdg)
    dila_id = uuid4()

    result = _upsert(_data("DILA", "dila-1", entity_id=dila_id))

    assert result["created"] == 1
    assert not OrganismeModel.objects.filter(id=gipcdg.id).exists()
    for model in (agent_link, recrutement, talentsoft, tag):
        model.refresh_from_db()
        assert model.organisme_id == dila_id
    child.refresh_from_db()
    assert child.parent_id == dila_id


def test_dependents_are_merged_into_an_existing_organisme():
    gipcdg = OrganismeDjangoFactory(siret=SIRET_A, referentiel="GIPCDG")
    dila = OrganismeDjangoFactory(
        siret=SIRET_B, referentiel="DILA", external_id="dila-1"
    )
    shared_agent_link = OrganismeAgentDjangoFactory(organisme=dila)
    OrganismeAgentDjangoFactory(organisme=gipcdg, agent=shared_agent_link.agent)
    other_agent_link = OrganismeAgentDjangoFactory(organisme=gipcdg)
    dila_tag = TagDjangoFactory(organisme=dila, name="Urgent")
    gipcdg_tag = TagDjangoFactory(organisme=gipcdg, name="URGENT")
    candidature_tag = CandidatureTagDjangoFactory(tag=gipcdg_tag)

    result = _upsert(_data("DILA", "dila-1", entity_id=dila.id))

    assert result["updated"] == 1
    assert not OrganismeModel.objects.filter(id=gipcdg.id).exists()
    assert _siret_holder().id == dila.id
    assert set(
        OrganismeAgentModel.objects.filter(organisme=dila).values_list(
            "agent_id", flat=True
        )
    ) == {shared_agent_link.agent_id, other_agent_link.agent_id}
    assert list(TagModel.objects.filter(organisme=dila)) == [dila_tag]
    candidature_tag.refresh_from_db()
    assert candidature_tag.tag_id == dila_tag.id


def test_update_to_an_already_held_siret_is_rejected():
    _upsert(_data("DILA", "dila-1"))
    _upsert(_data("DILA", "dila-2", siret=SIRET(code=SIRET_B)))

    result = _upsert(_data("DILA", "dila-2"))

    assert result["updated"] == 0
    assert len(result["errors"]) == 1
    holder = _siret_holder()
    assert holder.external_id == "dila-1"


def test_organismes_without_conflict_in_the_batch_are_created():
    _upsert(_data("DILA", "dila-1"))

    result = _upsert(
        _data("GIPCDG", "gip-1"),
        _data("GIPCDG", "gip-2", siret=SIRET(code=SIRET_B)),
    )

    assert result["created"] == 1
    assert len(result["errors"]) == 1
    assert _siret_holder(SIRET_B).external_id == "gip-2"
