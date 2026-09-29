import pytest
from referentiel.exceptions.offer_errors import OfferDoesNotExist

from application.ingestion.interfaces.get_offer_by_reference_input import (
    GetOfferByReferenceInput,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


def test_returns_offer_matching_reference(db, ingestion_container):
    offer = OfferDjangoFactory(reference="REF-1")
    OfferDjangoFactory(reference="REF-2")

    input_data = GetOfferByReferenceInput(reference="REF-1")
    result = ingestion_container.get_offer_by_reference_usecase().execute(input_data)

    assert result.id == offer.id
    assert result.talentsoft_organisme is None


def test_loads_talentsoft_organisme_with_offer(
    db, ingestion_container, django_assert_num_queries
):
    talentsoft_organisme = TalentsoftOrganismeDjangoFactory(
        entity_code="ENT-1", code=1, name="Commune de Paris", post_code="75001"
    )
    OfferDjangoFactory(
        reference="REF-1", talentsoft_organisme_entity_code=talentsoft_organisme
    )
    usecase = ingestion_container.get_offer_by_reference_usecase()

    with django_assert_num_queries(1):
        result = usecase.execute(GetOfferByReferenceInput(reference="REF-1"))

    assert result.talentsoft_organisme is not None
    assert result.talentsoft_organisme.entity_code == "ENT-1"
    assert result.talentsoft_organisme.name == "Commune de Paris"
    assert result.talentsoft_organisme.post_code == "75001"


def test_unknown_reference_raises(db, ingestion_container):
    input_data = GetOfferByReferenceInput(reference="UNKNOWN")

    with pytest.raises(OfferDoesNotExist):
        ingestion_container.get_offer_by_reference_usecase().execute(input_data)
