from enum import Enum


class Experience(Enum):
    DEBUTANT = "DEBUTANT"
    CONFIRME = "CONFIRME"
    EXPERT = "EXPERT"

    def __str__(self):
        return self.value
