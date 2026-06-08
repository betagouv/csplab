import logging
from datetime import datetime, timezone
from typing import cast

from application.use_cases.clean_raw_offer import CleanRawOfferUseCase
from application.use_cases.publish_offer import PublishOfferUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from domain.repositories.raw_offer_repository import IRawOfferRepository

logger = logging.getLogger(__name__)


class IngestOfferPipeline:
    def __init__(
        self,
        save_raw_offer: SaveRawOfferUseCase,
        clean_raw_offer: CleanRawOfferUseCase,
        raw_offer_repository: IRawOfferRepository,
        publish_offer: PublishOfferUseCase | None = None,
    ) -> None:
        self._save_raw_offer = save_raw_offer
        self._clean_raw_offer = clean_raw_offer
        self._raw_offer_repository = raw_offer_repository
        self._publish_offer = publish_offer

    async def execute(self, reference: str, source_id: str) -> None:
        raw_offer = await self._save_raw_offer.execute(reference, source_id)
        if raw_offer is None:
            return

        offer = None
        try:
            offer = self._clean_raw_offer.execute(raw_offer)
            await self._raw_offer_repository.mark_as_cleaned(
                cast(str, raw_offer.reference),
                cast(str, raw_offer.source_id),
                datetime.now(tz=timezone.utc),
            )
        except Exception:
            logger.exception("Failed to clean raw offer for reference %s", reference)

        if offer is None or self._publish_offer is None:
            return

        try:
            await self._publish_offer.execute(offer)
            await self._raw_offer_repository.mark_as_upserted(
                cast(str, raw_offer.reference),
                cast(str, raw_offer.source_id),
                datetime.now(tz=timezone.utc),
            )
        except Exception:
            logger.exception("Failed to publish offer for reference %s", reference)
