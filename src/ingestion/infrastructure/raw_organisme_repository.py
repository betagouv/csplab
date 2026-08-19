import asyncio
from datetime import datetime
from uuid import UUID

from sqlalchemy import Engine, delete, or_, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, col, select

from domain.entities.raw_organisme import RawOrganisme
from domain.repositories.raw_organisme_repository import IRawOrganismeRepository
from infrastructure.models.raw_organisme import RawOrganismeModel


class RawOrganismeRepository(IRawOrganismeRepository):
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def upsert_batch(self, organismes: list[RawOrganisme]) -> None:
        if not organismes:
            return
        await asyncio.to_thread(self._upsert_batch_sync, organismes)

    def _upsert_batch_sync(self, organismes: list[RawOrganisme]) -> None:
        with Session(self._engine) as session:
            insert_stmt = pg_insert(RawOrganismeModel).values(
                [
                    RawOrganismeModel.values_from_entity(organisme)
                    for organisme in organismes
                ]
            )
            stmt = insert_stmt.on_conflict_do_update(
                constraint="uq_raw_organisme_referentiel_external_id",
                set_={
                    "millesime": insert_stmt.excluded.millesime,
                    "data": insert_stmt.excluded.data,
                    "error_msg": insert_stmt.excluded.error_msg,
                    "loaded_at": insert_stmt.excluded.loaded_at,
                    "cleaned_at": None,
                },
            )
            session.execute(stmt)
            session.commit()

    async def delete_missing(self, referentiel: str, loaded_before: datetime) -> int:
        return await asyncio.to_thread(
            self._delete_missing_sync, referentiel, loaded_before
        )

    def _delete_missing_sync(self, referentiel: str, loaded_before: datetime) -> int:
        with Session(self._engine) as session:
            result = session.execute(
                delete(RawOrganismeModel).where(
                    col(RawOrganismeModel.referentiel) == referentiel,
                    or_(
                        col(RawOrganismeModel.loaded_at).is_(None),
                        col(RawOrganismeModel.loaded_at) < loaded_before,
                    ),
                )
            )
            session.commit()
            return result.rowcount  # type: ignore[attr-defined]

    async def find_uncleaned(self, referentiel: str, limit: int) -> list[RawOrganisme]:
        return await asyncio.to_thread(self._find_uncleaned_sync, referentiel, limit)

    def _find_uncleaned_sync(self, referentiel: str, limit: int) -> list[RawOrganisme]:
        with Session(self._engine) as session:
            statement = (
                select(RawOrganismeModel)
                .where(
                    col(RawOrganismeModel.referentiel) == referentiel,
                    col(RawOrganismeModel.cleaned_at).is_(None),
                )
                .limit(limit)
            )
            rows = session.exec(statement).all()
            return [row.to_entity() for row in rows]

    async def mark_as_cleaned_batch(
        self, ids: list[UUID], cleaned_at: datetime
    ) -> None:
        if not ids:
            return
        await asyncio.to_thread(self._mark_as_cleaned_batch_sync, ids, cleaned_at)

    def _mark_as_cleaned_batch_sync(
        self, ids: list[UUID], cleaned_at: datetime
    ) -> None:
        with Session(self._engine) as session:
            session.execute(
                update(RawOrganismeModel)
                .where(col(RawOrganismeModel.id).in_(ids))
                .values(cleaned_at=cleaned_at)
            )
            session.commit()
