import asyncio
from datetime import datetime, timezone

from sqlalchemy import Engine, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, col

from domain.entities.raw_offer import RawOffer
from domain.repositories.raw_offer_repository import IRawOfferRepository
from infrastructure.models.raw_offer import RawOfferModel


class RawOfferRepository(IRawOfferRepository):
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def upsert(self, offer: RawOffer) -> None:
        await asyncio.to_thread(self._upsert_sync, offer)

    def _upsert_sync(self, offer: RawOffer) -> None:
        now = datetime.now(tz=timezone.utc)
        with Session(self._engine) as session:
            stmt = (
                pg_insert(RawOfferModel)
                .values(
                    id=offer.id,
                    created_at=now,
                    updated_at=now,
                    reference=offer.reference,
                    source_id=offer.source_id,
                    data=offer.data,
                    error_msg=offer.error_msg,
                    loaded_at=offer.loaded_at,
                    cleaned_at=offer.cleaned_at,
                    upsert_at=None,
                )
                .on_conflict_do_update(
                    constraint="uq_raw_offer_reference_source",
                    set_={
                        "updated_at": now,
                        "data": offer.data,
                        "error_msg": offer.error_msg,
                        "loaded_at": offer.loaded_at,
                    },
                )
            )
            session.execute(stmt)
            session.commit()

    async def mark_as_cleaned(
        self, reference: str, source_id: str, cleaned_at: datetime
    ) -> None:
        await asyncio.to_thread(
            self._mark_as_cleaned_sync, reference, source_id, cleaned_at
        )

    def _mark_as_cleaned_sync(
        self, reference: str, source_id: str, cleaned_at: datetime
    ) -> None:
        now = datetime.now(tz=timezone.utc)
        with Session(self._engine) as session:
            result = session.execute(
                update(RawOfferModel)
                .where(
                    col(RawOfferModel.reference) == reference,
                    col(RawOfferModel.source_id) == source_id,
                )
                .values(cleaned_at=cleaned_at, updated_at=now)
            )
            if result.rowcount == 0:  # type: ignore[attr-defined]
                raise ValueError(
                    f"RawOffer not found for reference={reference},"
                    f" source_id={source_id}"
                )
            session.commit()
