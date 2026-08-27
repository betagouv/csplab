from uuid import uuid4

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)


class OrganismeRecruteurFactory:
    @staticmethod
    def create_entity(
        etapes: tuple[EtapeRecrutement, ...] | None = None,
    ) -> OrganismeRecruteur:
        return OrganismeRecruteur.build(
            entity_id=uuid4(),
            etapes=etapes or EtapeRecrutementFactory.create_entity_batch(),
        )
