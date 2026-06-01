import logging
from datetime import datetime, timezone
from typing import Any

from domain.entities.raw_offer import RawOffer
from domain.gateways.offers_gateway import IOffersGateway
from domain.repositories.raw_offer_repository import IRawOfferRepository

logger = logging.getLogger(__name__)


class SaveRawOfferUseCase:
    def __init__(
        self,
        offers_gateway: IOffersGateway,
        raw_offer_repository: IRawOfferRepository,
    ) -> None:
        self._offers_gateway = offers_gateway
        self._raw_offer_repository = raw_offer_repository

    async def execute(self, reference: str, source_id: str) -> None:
        error_msg: str | None = None
        loaded_at: datetime | None = None
        data: dict[str, Any] | None = None
        try:
            offer = await self._offers_gateway.get_detail(reference)
            loaded_at = datetime.now(tz=timezone.utc)
            data = offer.data
        except Exception as e:
            error_msg = str(e)
            raise
        finally:
            try:
                await self._raw_offer_repository.upsert(
                    RawOffer(
                        reference=reference,
                        source_id=source_id,
                        data=data,
                        error_msg=error_msg,
                        loaded_at=loaded_at,
                    )
                )
            except Exception:
                logger.exception("Failed to save raw offer for reference %s", reference)
