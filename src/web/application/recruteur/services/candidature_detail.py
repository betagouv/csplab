from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class EtapeDetailStub:
    etape_id: UUID
    nom: str


@dataclass(frozen=True, kw_only=True)
class CandidatDetailStub:
    id: UUID
    prenom: str
    nom: str
    email: str


@dataclass(frozen=True, kw_only=True)
class CandidatureDetailStub:
    candidature_id: UUID
    candidat: CandidatDetailStub
    recrutement_intitule: str
    etapes: list[EtapeDetailStub]
    etape_actuelle: EtapeDetailStub
    date_candidature: datetime
    date_derniere_maj_candidat: datetime | None
    date_derniere_maj_recruteur: datetime | None
    document_id: UUID
    navigation_candidature_ids: list[UUID]


# TODO(#1440 suite) : remplacer par une vraie requête + les gardes organisme/
# recrutement/rôle une fois le frontend câblé sur la forme de ce payload.
def get_candidature_detail_stub(
    *, organisme_id: UUID, recrutement_id: UUID, candidature_id: UUID
) -> CandidatureDetailStub:
    etapes = [
        EtapeDetailStub(etape_id=uuid4(), nom="Candidatures reçues"),
        EtapeDetailStub(etape_id=uuid4(), nom="Entretien"),
        EtapeDetailStub(etape_id=uuid4(), nom="Décision"),
    ]
    return CandidatureDetailStub(
        candidature_id=candidature_id,
        candidat=CandidatDetailStub(
            id=uuid4(),
            prenom="Jean",
            nom="Dupont",
            email="jean.dupont@example.com",
        ),
        recrutement_intitule="Chargé de recrutement",
        etapes=etapes,
        etape_actuelle=etapes[1],
        date_candidature=datetime(2026, 8, 1, tzinfo=timezone.utc),
        date_derniere_maj_candidat=datetime(2026, 8, 3, tzinfo=timezone.utc),
        date_derniere_maj_recruteur=datetime(2026, 8, 5, tzinfo=timezone.utc),
        document_id=uuid4(),
        navigation_candidature_ids=[uuid4(), candidature_id, uuid4()],
    )
