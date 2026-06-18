from enum import Enum


class ContractType(Enum):
    TITULAIRE_CONTRACTUEL = "TITULAIRE_CONTRACTUEL"
    CONTRACTUELS = "CONTRACTUELS"
    TERRITORIAL = "TERRITORIAL"

    def __str__(self):
        return self.value


class ContractKind(Enum):
    CDD = "CDD"
    CDI = "CDI"
    PERMANENT = "Permanent"
    VACATION = "Vacation"
    STAGE = "Stage"
