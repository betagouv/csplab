import pytest

from domain.value_objects.opportunity_type import OpportunityType
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.metier_factory import MetierFactory
from tests.factories.offer_factory import OfferFactory


@pytest.mark.parametrize(
    ("offer_family_code", "metier_family_code", "expected_metiers_count"),
    [
        pytest.param("ERJUR011", "ERJUR011", 1, id="nominal_case"),
        pytest.param(None, "ERJUR011", 0, id="no_family_code"),
        pytest.param("ERJUR011", "ERJUR022", 0, id="no_matching_metiers"),
    ],
)
def test_execute_get_offer_details(
    get_opportunity_details_usecase,
    offer_family_code,
    metier_family_code,
    expected_metiers_count,
):
    offer = OfferFactory.create_entity(family_code=offer_family_code)
    offer_repo = get_opportunity_details_usecase.offers_repository
    offer_repo.upsert_batch([offer])

    metier = MetierFactory.create_entity(offer_family_code=metier_family_code)
    metier_repo = get_opportunity_details_usecase.metiers_repository
    metier_repo.upsert_batch([metier])

    result_offer, result_metiers = get_opportunity_details_usecase.execute(
        opportunity_type=OpportunityType.OFFER, opportunity_id=offer.id
    )

    assert result_offer.id == offer.id
    assert len(result_metiers) == expected_metiers_count


def test_execute_get_concours_details(
    get_opportunity_details_usecase,
):
    concours = ConcoursFactory.create_entity()
    concours_repo = get_opportunity_details_usecase.concours_repository
    concours_repo.upsert_batch([concours])

    result_concours = get_opportunity_details_usecase.execute(
        opportunity_type=OpportunityType.CONCOURS, opportunity_id=concours.id
    )

    assert result_concours.id == concours.id
