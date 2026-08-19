from enum import Enum


class GeographicalArea(Enum):
    AFRIQUE = "AF"
    EUROPE = "EU"
    ASIE = "AS"
    AMERIQUE = "AM"
    OCEANIE = "OC"
    ANTARTIQUE = "AN"
    MOYEN_ORIENT_AFRIQUE_DU_NORD = "MO"

    def __str__(self):
        return self.value
