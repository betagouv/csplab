from polyfactory.factories.dataclass_factory import DataclassFactory

from domain.recrutement.entities.organisme import Organisme
from domain.shared.value_objects.etapes_recrutement import (
    EtapesRecrutement,
)
from tests.ats.shared.factories.shared_factories import make_etapes_recrutement


class OrganismeFactory:
    @staticmethod
    def build(
        parametres: EtapesRecrutement | None = None,
    ) -> "Organisme":
        return Organisme.build(
            parametres=parametres or make_etapes_recrutement(),
        )
