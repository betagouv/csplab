from enum import Enum


class SourceType(Enum):
    TALENTSOFT = "talentsoft"
    API = "api"

    def __str__(self) -> str:
        return self.value
