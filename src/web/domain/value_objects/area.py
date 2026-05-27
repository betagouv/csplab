from enum import Enum


class GeographicalArea(Enum):
    AFRIQUE = "AF"
    EUROPE = "EU"
    ASIE = "AS"
    AMERIQUE = "AM"
    OCEANIE = "OC"
    ANTARTIQUE = "AN"

    def __str__(self):
        return self.value
