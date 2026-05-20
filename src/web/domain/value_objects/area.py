from enum import Enum


class GeographicalArea(Enum):
    AF = "AF", "Africa"
    EU = "EU", "Europe"
    AS = "AS", "Asia"
    AM = "AM", "America-Caribbean"
    AU = "AU", "Australia-Oceania"
    AN = "AN", "Antarctica"

    label: str

    def __new__(cls, code: str, label: str = ""):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.label = label
        return obj

    def __str__(self):
        return self.value


TALENTSOFT_TO_AREA: dict[str, GeographicalArea] = {
    "_TS_CO_GeographicalArea_Afrique": GeographicalArea.AF,
    "_TS_CO_GeographicalArea_AmriquesCaraibe": GeographicalArea.AM,
    "_TS_CO_GeographicalArea_Asie": GeographicalArea.AS,
    "_TS_CO_GeographicalArea_Europe": GeographicalArea.EU,
    "_TS_CO_GeographicalArea_MoyenOrientAfriqueduNord": GeographicalArea.AF,
    "_TS_CO_GeographicalArea_Ocanie": GeographicalArea.AU,
}


def get_talentsoft_area(code: str) -> GeographicalArea | None:
    return TALENTSOFT_TO_AREA.get(code)
