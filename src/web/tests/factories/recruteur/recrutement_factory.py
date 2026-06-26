from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.position_candidature import PositionCandidature
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from tests.factories.recruteur.organisme_factory import make_etapes_recrutement


class PositionCandidatureFactory:
    @staticmethod
    def create_entity(
        candidature_id: UUID | None = None,
        etape_id: UUID | None = None,
        ordre: int | None = None,
    ) -> PositionCandidature:
        return PositionCandidature(
            candidature_id=candidature_id or uuid4(),
            etape_id=etape_id or uuid4(),
            ordre=ordre,
        )


class RecrutementFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        offre_id: UUID | None = None,
        organisme_id: UUID | None = None,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
        status: RecrutementStatus = RecrutementStatus.ACTIF,
        positions: tuple[PositionCandidature, ...] = (),
        responsables_ids: tuple[UUID, ...] = (),
        derniere_activite_le: datetime | None = None,
        candidat_recrute_id: UUID | None = None,
    ) -> Recrutement:
        return Recrutement.build(
            entity_id=entity_id or uuid4(),
            offre_id=offre_id or uuid4(),
            organisme_id=organisme_id or uuid4(),
            etapes=etapes or make_etapes_recrutement(),
            status=status,
            positions=positions,
            responsables_ids=responsables_ids,
            derniere_activite_le=derniere_activite_le or datetime.now(tz=timezone.utc),
            candidat_recrute_id=candidat_recrute_id,
        )
