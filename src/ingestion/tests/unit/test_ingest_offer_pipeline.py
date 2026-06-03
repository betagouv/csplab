from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from application.pipelines.ingest_offer_pipeline import IngestOfferPipeline
from application.use_cases.clean_raw_offer import CleanRawOfferUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from domain.entities.raw_offer import RawOffer
from infrastructure.exceptions.exceptions import ExternalApiError

REFERENCE = "2024-OFFER-001"
SOURCE_ID = "11111111-2222-3333-4444-555555555555"
RAW_OFFER = RawOffer(
    reference=REFERENCE,
    source_id=SOURCE_ID,
    data={"reference": REFERENCE},
)


@pytest.fixture
def mock_save_use_case():
    use_case = MagicMock(spec=SaveRawOfferUseCase)
    use_case.execute = AsyncMock(return_value=RAW_OFFER)
    return use_case


@pytest.fixture
def mock_clean_use_case():
    return MagicMock(spec=CleanRawOfferUseCase)


@pytest.fixture
def mock_raw_offer_repository():
    repo = MagicMock()
    repo.mark_as_cleaned = AsyncMock()
    return repo


@pytest.fixture
def pipeline(
    mock_save_use_case, mock_clean_use_case, mock_raw_offer_repository
) -> IngestOfferPipeline:
    return IngestOfferPipeline(
        save_raw_offer=mock_save_use_case,
        clean_raw_offer=mock_clean_use_case,
        raw_offer_repository=mock_raw_offer_repository,
    )


@pytest.mark.asyncio
async def test_execute_calls_save_then_clean(
    pipeline, mock_save_use_case, mock_clean_use_case
):
    await pipeline.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_save_use_case.execute.assert_awaited_once_with(REFERENCE, SOURCE_ID)
    mock_clean_use_case.execute.assert_called_once_with(RAW_OFFER)


@pytest.mark.asyncio
async def test_execute_marks_as_cleaned_on_success(
    pipeline, mock_clean_use_case, mock_raw_offer_repository
):
    await pipeline.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_clean_use_case.execute.assert_called_once_with(RAW_OFFER)
    mock_raw_offer_repository.mark_as_cleaned.assert_awaited_once()
    call_args = mock_raw_offer_repository.mark_as_cleaned.call_args
    assert call_args[0][0] == REFERENCE
    assert call_args[0][1] == SOURCE_ID


@pytest.mark.asyncio
async def test_execute_skips_clean_when_save_returns_none(
    pipeline, mock_save_use_case, mock_clean_use_case, mock_raw_offer_repository
):
    mock_save_use_case.execute.return_value = None

    await pipeline.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_clean_use_case.execute.assert_not_called()
    mock_raw_offer_repository.mark_as_cleaned.assert_not_called()


@pytest.mark.asyncio
async def test_execute_propagates_save_error(
    pipeline, mock_save_use_case, mock_clean_use_case, mock_raw_offer_repository
):
    mock_save_use_case.execute.side_effect = ExternalApiError(
        message="API down", api_name="Talentsoft"
    )

    with pytest.raises(ExternalApiError):
        await pipeline.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_clean_use_case.execute.assert_not_called()
    mock_raw_offer_repository.mark_as_cleaned.assert_not_called()


@pytest.mark.asyncio
async def test_execute_does_not_raise_when_clean_fails(
    pipeline, mock_save_use_case, mock_clean_use_case, mock_raw_offer_repository
):
    mock_clean_use_case.execute.side_effect = ValueError("Bad data")

    with patch("application.pipelines.ingest_offer_pipeline.logger") as mock_logger:
        await pipeline.execute(reference=REFERENCE, source_id=SOURCE_ID)
        mock_logger.exception.assert_called_once()

    mock_raw_offer_repository.mark_as_cleaned.assert_not_called()


@pytest.mark.asyncio
async def test_execute_does_not_raise_when_mark_as_cleaned_fails(
    pipeline, mock_clean_use_case, mock_raw_offer_repository
):
    mock_raw_offer_repository.mark_as_cleaned.side_effect = RuntimeError("DB down")

    with patch("application.pipelines.ingest_offer_pipeline.logger") as mock_logger:
        await pipeline.execute(reference=REFERENCE, source_id=SOURCE_ID)
        mock_logger.exception.assert_called_once()
