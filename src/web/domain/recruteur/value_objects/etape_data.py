from uuid import UUID

from pydantic import dataclasses

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class EtapeData:
    etape_uuid: UUID | None
    nom: str
    categorie: CategorieEtapeRecrutement
