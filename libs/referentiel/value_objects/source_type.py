from enum import Enum


class SourceType(Enum):
    TALENTSOFT = "talentsoft"
    API = "api"

    def __str__(self):
        return self.value
