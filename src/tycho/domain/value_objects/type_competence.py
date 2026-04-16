from enum import Enum


class TypeCompetence(Enum):
    SAVOIR_FAIRE = "SAVOIR_FAIRE"
    SAVOIR_ETRE = "SAVOIR_ETRE"
    CONNAISSANCE = "CONNAISSANCE"

    def __str__(self):
        return self.value
