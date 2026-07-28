from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(frozen=True, kw_only=True)
class EtapeData:
    etape_uuid: UUID | None
    nom: str
    categorie: CategorieEtapeRecrutement


def etapes_par_defaut() -> list[EtapeData]:
    return [
        EtapeData(
            etape_uuid=uuid4(),
            nom="Réception des candidatures",
            categorie=CategorieEtapeRecrutement.ENTREE,
        ),
        EtapeData(
            etape_uuid=uuid4(),
            nom="Présélection",
            categorie=CategorieEtapeRecrutement.EN_COURS,
        ),
        EtapeData(
            etape_uuid=uuid4(),
            nom="Entretien",
            categorie=CategorieEtapeRecrutement.EN_COURS,
        ),
        EtapeData(
            etape_uuid=uuid4(),
            nom="Proposition",
            categorie=CategorieEtapeRecrutement.EN_COURS,
        ),
        EtapeData(
            etape_uuid=uuid4(),
            nom="Refus",
            categorie=CategorieEtapeRecrutement.REFUS,
        ),
        EtapeData(
            etape_uuid=uuid4(),
            nom="Recrutement",
            categorie=CategorieEtapeRecrutement.ACCEPTE,
        ),
    ]
