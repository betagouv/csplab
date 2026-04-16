from dataclasses import dataclass

from domain.value_objects.type_competence import TypeCompetence


@dataclass(frozen=True)
class Competence:
    code: str
    libelle: str
    description: str
    type_competence: TypeCompetence
