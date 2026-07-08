from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur


class CandidatureFactory:
    @staticmethod
    def create_entity(
        recrutement_id: UUID | None = None,
        candidat_id: UUID | None = None,
        etapes_id: UUID | None = None,
        derniere_activite_le: datetime | None = None,
    ) -> CandidatureRecruteur:
        return CandidatureRecruteur.build(
            recrutement_id=recrutement_id or uuid4(),
            candidat_id=candidat_id or uuid4(),
            etapes_id=etapes_id or uuid4(),
            derniere_activite_le=derniere_activite_le or datetime.now(tz=timezone.utc),
        )
