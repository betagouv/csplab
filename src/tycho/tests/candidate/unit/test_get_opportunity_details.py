from domain.value_objects.opportunity_type import OpportunityType
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.metier_factory import MetierFactory
from tests.factories.offer_factory import OfferFactory


def test_execute_get_offer_details(
    get_opportunity_details_usecase,
):
    offer = OfferFactory.create_entity(family_code="ERJUR011")
    offer_repo = get_opportunity_details_usecase.offers_repository
    offer_repo.upsert_batch([offer])

    metier = MetierFactory.create_entity(offer_family_code="ERJUR011")
    metier_repo = get_opportunity_details_usecase.metiers_repository
    metier_repo.upsert_batch([metier])

    result_offer, result_metiers = get_opportunity_details_usecase.execute(
        opportunity_type=OpportunityType.OFFER, opportunity_id=offer.id
    )

    assert result_offer.id == offer.id
    assert len(result_metiers) == 1
    assert result_metiers[0].offer_family_code == offer.family_code


def test_execute_get_offer_details_no_family_code(
    get_opportunity_details_usecase,
):
    offer = OfferFactory.create_entity(family_code=None)
    offer_repo = get_opportunity_details_usecase.offers_repository
    offer_repo.upsert_batch([offer])

    metier = MetierFactory.create_entity(offer_family_code="ERJUR011")
    metier_repo = get_opportunity_details_usecase.metiers_repository
    metier_repo.upsert_batch([metier])

    result_offer, result_metiers = get_opportunity_details_usecase.execute(
        opportunity_type=OpportunityType.OFFER, opportunity_id=offer.id
    )

    assert result_offer.id == offer.id
    assert len(result_metiers) == 0


def test_execute_get_offer_details_no_metiers(
    get_opportunity_details_usecase,
):
    offer = OfferFactory.create_entity(family_code="ERJUR011")
    offer_repo = get_opportunity_details_usecase.offers_repository
    offer_repo.upsert_batch([offer])

    metier = MetierFactory.create_entity(offer_family_code="ERJUR022")
    metier_repo = get_opportunity_details_usecase.metiers_repository
    metier_repo.upsert_batch([metier])

    result_offer, result_metiers = get_opportunity_details_usecase.execute(
        opportunity_type=OpportunityType.OFFER, opportunity_id=offer.id
    )

    assert result_offer.id == offer.id
    assert len(result_metiers) == 0


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
