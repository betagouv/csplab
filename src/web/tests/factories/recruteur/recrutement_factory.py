from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from tests.factories.recruteur.etapes_recrutement_factory import EtapeRecrutementFactory


class RecrutementFactory:
    @staticmethod
    def create_entity(
        offre_id: UUID | None = None,
        organisme_id: UUID | None = None,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
        candidatures: tuple[UUID, ...] | None = None,
        responsables: tuple[UUID, ...] | None = None,
        status: StatutRecrutement | None = None,
        candidat_recrute_id: UUID | None = None,
        derniere_activite_le: datetime | None = None,
    ) -> Recrutement:
        return Recrutement.build(
            offre_id=offre_id or uuid4(),
            organisme_id=organisme_id or uuid4(),
            etapes=etapes or EtapeRecrutementFactory.create_entities(),
            candidatures=candidatures or (),
            responsables=responsables or (),
            status=status or StatutRecrutement.ACTIF,
            candidat_recrute_id=candidat_recrute_id,
            derniere_activite_le=derniere_activite_le or datetime.now(tz=timezone.utc),
        )
