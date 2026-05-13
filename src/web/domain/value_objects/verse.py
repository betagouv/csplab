from enum import Enum


class Verse(Enum):
    FPT = "FPT"
    FPE = "FPE"
    FPH = "FPH"

    def __str__(self):
        return self.value
