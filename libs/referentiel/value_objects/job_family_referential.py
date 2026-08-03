from enum import Enum


class JobFamilyReferential(Enum):
    RMFPV2 = "RMFPv2"

    def __str__(self):
        return self.value
