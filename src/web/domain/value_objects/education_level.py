from enum import Enum


class EducationLevel(Enum):
    A = "Brevet"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "Doctorant"

    def __str__(self):
        return self.value
