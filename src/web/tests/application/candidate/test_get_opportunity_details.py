from domain.candidate.value_objects.opportunity_type import OpportunityType
from infrastructure.factories.referentiel.concours_factory import ConcoursFactory


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
