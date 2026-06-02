from dataclasses import dataclass
from uuid import UUID

from domain.ddd.aggregate_root import AggregateRoot, factory
from domain.identite.events.organisme_events import (
    OrganismeCree,
)
from domain.identite.value_objects.siret import SIRET
from domain.value_objects.localisation import Localisation
from domain.value_objects.verse import Verse


@dataclass(kw_only=True)
class Organisme(AggregateRoot):
    _nom: str
    _versant: Verse
    _localisation: Localisation | None
    _siret: SIRET | None
    _parent_id: UUID | None

    @classmethod
    def build(
        cls,
        nom: str,
        versant: Verse,
        localisation: Localisation,
        siret: SIRET | None = None,
        parent_id: UUID | None = None,
    ) -> "Organisme":
        return cls(
            _nom=nom,
            _versant=versant,
            _localisation=localisation,
            _siret=siret,
            _parent_id=parent_id,
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

    @classmethod
    @factory(OrganismeCree)
    def create(cls, event: OrganismeCree) -> "Organisme":
        return cls(
            _nom=event.nom,
            _versant=event.versant,
            _localisation=event.localisation,
            _siret=event.siret,
            _parent_id=event.parent_id,
        )
