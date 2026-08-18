from dataclasses import dataclass
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse

from domain.identite.events.organisme_events import (
    OrganismeCree,
)
from domain.identite.value_objects.siret import SIRET


@dataclass(kw_only=True)
class Organisme(AggregateRoot):
    _nom: str
    _versant: Verse
    _localisation: Localisation | None
    _siret: SIRET
    _parent_id: UUID | None
    _external_id: str | None
    _referentiel: str | None
    _millesime: str | None

    @classmethod
    def build(
        cls,
        entity_id: UUID,
        nom: str,
        versant: Verse,
        localisation: Localisation | None,
        siret: SIRET,
        parent_id: UUID | None = None,
        external_id: str | None = None,
        referentiel: str | None = None,
        millesime: str | None = None,
    ) -> "Organisme":
        return cls(
            entity_id=entity_id,
            _nom=nom,
            _versant=versant,
            _localisation=localisation,
            _siret=siret,
            _parent_id=parent_id,
            _external_id=external_id,
            _referentiel=referentiel,
            _millesime=millesime,
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
    def siret(self) -> SIRET:
        return self._siret

    @property
    def parent_id(self) -> UUID | None:
        return self._parent_id

    @property
    def external_id(self) -> str | None:
        return self._external_id

    @property
    def referentiel(self) -> str | None:
        return self._referentiel

    @property
    def millesime(self) -> str | None:
        return self._millesime

    @classmethod
    @factory(OrganismeCree)
    def create(
        cls,
        nom: str,
        versant: Verse,
        localisation: Localisation | None,
        siret: SIRET,
        parent_id: UUID | None,
        external_id: str | None = None,
        referentiel: str | None = None,
        millesime: str | None = None,
    ) -> "Organisme":
        return cls(
            _nom=nom,
            _versant=versant,
            _localisation=localisation,
            _siret=siret,
            _parent_id=parent_id,
            _external_id=external_id,
            _referentiel=referentiel,
            _millesime=millesime,
        )
