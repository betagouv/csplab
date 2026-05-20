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
