from datetime import datetime, timezone

from application.usecases.clean_raw_offer import CleanRawOfferUsecase
from application.usecases.publish_offer import PublishOfferUsecase
from application.usecases.save_raw_offer import SaveRawOfferUsecase
from domain.repositories.raw_offer_repository import IRawOfferRepository


class IngestOfferPipeline:
    def __init__(
        self,
        save_raw_offer: SaveRawOfferUsecase,
        clean_raw_offer: CleanRawOfferUsecase,
        raw_offer_repository: IRawOfferRepository,
        publish_offer: PublishOfferUsecase | None = None,
    ) -> None:
        self._save_raw_offer = save_raw_offer
        self._clean_raw_offer = clean_raw_offer
        self._raw_offer_repository = raw_offer_repository
        self._publish_offer = publish_offer

    async def execute(self, reference: str, source_id: str) -> None:
        raw_offer = await self._save_raw_offer.execute(reference, source_id)
        offer = self._clean_raw_offer.execute(raw_offer)
        await self._raw_offer_repository.mark_as_cleaned(
            reference, source_id, datetime.now(tz=timezone.utc)
        )
        if self._publish_offer is None:
            return

        try:
            await self._publish_offer.execute(offer)
        except Exception as exc:
            await self._raw_offer_repository.mark_as_publish_failed(
                reference, source_id, str(exc)
            )
            raise
        await self._raw_offer_repository.mark_as_upserted(
            reference, source_id, datetime.now(tz=timezone.utc)
        )
