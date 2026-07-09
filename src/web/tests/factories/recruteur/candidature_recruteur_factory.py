from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur


class CandidatureRecruteurFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        candidat_id: UUID | None = None,
        recrutement_id: UUID | None = None,
        etape_id: UUID | None = None,
        derniere_activite_le: datetime | None = None,
    ) -> CandidatureRecruteur:
        return CandidatureRecruteur.build(
            entity_id=entity_id or uuid4(),
            candidat_id=candidat_id or uuid4(),
            recrutement_id=recrutement_id or uuid4(),
            etape_id=etape_id or uuid4(),
            derniere_activite_le=derniere_activite_le or datetime.now(tz=timezone.utc),
        )
