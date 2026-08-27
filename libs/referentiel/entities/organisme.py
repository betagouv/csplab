from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot, factory, mutate

from referentiel.events.organisme_events import (
    OrganismeCree,
    OrganismeModifie,
    OrganismeRemplace,
)
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


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
    _gestion_ats: bool | None
    _date_creation: datetime | None
    _date_derniere_activite: datetime | None

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
        date_creation: datetime | None = None,
        date_derniere_activite: datetime | None = None,
        gestion_ats: bool | None = False,
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
            _gestion_ats=gestion_ats,
            _date_creation=date_creation,
            _date_derniere_activite=date_derniere_activite,
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

    @property
    def gestion_ats(self) -> bool | None:
        return self._gestion_ats

    @property
    def date_creation(self) -> datetime | None:
        return self._date_creation

    @property
    def date_derniere_activite(self) -> datetime | None:
        return self._date_derniere_activite

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
        gestion_ats: bool | None = False,
        entity_id: UUID | None = None,
    ) -> "Organisme":
        return cls(
            **({"entity_id": entity_id} if entity_id is not None else {}),
            _nom=nom,
            _versant=versant,
            _localisation=localisation,
            _siret=siret,
            _parent_id=parent_id,
            _external_id=external_id,
            _referentiel=referentiel,
            _millesime=millesime,
            _gestion_ats=gestion_ats,
            _date_creation=datetime.now(tz=timezone.utc),
            _date_derniere_activite=datetime.now(tz=timezone.utc),
        )

    @mutate(OrganismeModifie)
    def modifier(
        self,
        nom: str | None,
        versant: Verse | None,
        gestion_ats: bool | None,
    ) -> None:
        if nom is not None:
            self._nom = nom
        if versant is not None:
            self._versant = versant
        if gestion_ats is not None:
            self._gestion_ats = gestion_ats
        self._date_derniere_activite = datetime.now(tz=timezone.utc)

    @mutate(OrganismeRemplace)
    def remplacer(
        self,
        *,
        nom: str,
        versant: Verse,
        localisation: Localisation | None,
        siret: SIRET,
        parent_id: UUID | None,
        external_id: str | None = None,
        referentiel: str | None = None,
        millesime: str | None = None,
        gestion_ats: bool | None = False,
        date_creation: datetime | None = None,
        date_derniere_activite: datetime | None = None,
    ) -> None:
        self._nom = nom
        self._versant = versant
        self._localisation = localisation
        self._siret = siret
        self._parent_id = parent_id
        self._external_id = external_id
        self._referentiel = referentiel
        self._millesime = millesime
        self._gestion_ats = gestion_ats
        self._date_creation = date_creation
        self._date_derniere_activite = date_derniere_activite
