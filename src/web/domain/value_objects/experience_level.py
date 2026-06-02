from enum import Enum


class ExperienceLevel(Enum):
    DEBUTANT = "Débutant"
    CONFIRME = "Confirmé"
    EXPERT = "Expert"

    def __str__(self):
        return self.value
