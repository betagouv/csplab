from faker import Faker
from application.ingestion.usecases.list_offers import (
    GetOffersCommand,
    ListOffersUseCase,
)
from tests.factories.offer_factory import OfferFactory


OFFERS_COUNT = 5


@pytest.fixture(name="mock_repository")
def mock_repository_fixture():
    mock = MagicMock()
    mock.get_by_status_and_period.return_value = [
        OfferFactory.build() for _ in range(OFFERS_COUNT)
    ]
    return mock


class TestListOffersUseCase:
    def test_returns_list_of_offers(self, mock_repository):
        usecase = ListOffersUseCase(offers_repository=mock_repository)
        result = usecase.execute(GetOffersCommand(active=True, after=None, before=None))
        assert result.offers == mock_repository.get_by_status_and_period.return_value
