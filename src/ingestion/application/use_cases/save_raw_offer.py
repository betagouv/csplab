import logging
from datetime import datetime, timezone
from typing import Any

from application.interfaces.raw_offer_repository import IRawOfferRepository
from application.interfaces.talentsoft_client_interface import ITalentsoftFrontClient
from infrastructure.models.raw_offer import RawOffer

logger = logging.getLogger(__name__)


class SaveRawOfferUseCase:
    def __init__(
        self,
        talentsoft_client: ITalentsoftFrontClient,
        raw_offer_repository: IRawOfferRepository,
    ) -> None:
        self._talentsoft_client = talentsoft_client
        self._raw_offer_repository = raw_offer_repository

    async def execute(self, reference: str, source_id: str) -> None:
        error_msg: str | None = None
        loaded_at: datetime | None = None
        data: dict[str, Any] | None = None
        try:
            offer = await self._talentsoft_client.get_detail(reference)
            loaded_at = datetime.now(tz=timezone.utc)
            data = offer.model_dump()
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
