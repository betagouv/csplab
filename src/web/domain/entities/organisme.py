from dataclasses import dataclass
from uuid import UUID

from domain.ddd.aggregate_root import AggregateRoot, mutate
from domain.events.organisme_events import ConfigRecrutementAjoute
from domain.value_objects.localisation import Localisation
from domain.value_objects.siret import SIRET
from domain.value_objects.verse import Verse


@dataclass(kw_only=True)
class Organisme(AggregateRoot):
    _nom: str
    _versant: Verse
    _localisation: Localisation | None
    _siret: SIRET | None
    _parent_id: UUID | None
    _config_recrutement: list[str]

    @classmethod
    def build(
        cls,
        nom: str,
        versant: Verse,
        localisation: Localisation,
        config_recrutement: list[str],
        siret: SIRET | None = None,
        parent_id: UUID | None = None,
    ) -> "Organisme":
        return cls(
            _nom=nom,
            _versant=versant,
            _localisation=localisation,
            _siret=siret,
            _parent_id=parent_id,
            _config_recrutement=config_recrutement,
        )

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def versant(self) -> Verse:
        return self._versant

    @property
    def localisation(self) -> Localisation | None:
        return self._localisation

    @property
    def siret(self) -> SIRET | None:
        return self._siret

    @property
    def parent_id(self) -> UUID | None:
        return self._parent_id

    @property
    def config_recrutement(self) -> list[str]:
        return self._config_recrutement

    @mutate(ConfigRecrutementAjoute)
    def add_default_config_recrutement(self, event: ConfigRecrutementAjoute) -> None:
        for item in event.config:
            if item not in self._config_recrutement:
                self._config_recrutement.append(item)
