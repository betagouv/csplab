from enum import Enum


class ExperienceLevel(Enum):
    A = "Débutant"
    B = "Confirmé"
    C = "Expert"

    def __str__(self):
        return self.value
