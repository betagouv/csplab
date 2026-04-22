from dataclasses import dataclass

from domain.value_objects.type_competence import TypeCompetence


@dataclass(frozen=True)
class Competence:
    libelle: str
    type_competence: TypeCompetence
