from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class PositionCandidature:
    candidature_id: UUID
    etape_id: UUID
    ordre: int | None = None  # None = sort by date; int = manual rank in column
