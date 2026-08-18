from dataclasses import dataclass

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region


@dataclass(frozen=True)
class RegionEtZone:
    region: Region
    area: GeographicalArea


_DEPARTEMENT_VERS_REGION: dict[str, RegionEtZone] = {}


def _register(code_region: str, area: GeographicalArea, *departements: str) -> None:
    for departement in departements:
        _DEPARTEMENT_VERS_REGION[departement] = RegionEtZone(
            region=Region(code=code_region), area=area
        )


_register(
    "84",
    GeographicalArea.EUROPE,
    "01",
    "03",
    "07",
    "15",
    "26",
    "38",
    "42",
    "43",
    "63",
    "69",
    "73",
    "74",
)
_register(
    "27", GeographicalArea.EUROPE, "21", "25", "39", "58", "70", "71", "89", "90"
)
_register("53", GeographicalArea.EUROPE, "22", "29", "35", "56")
_register("24", GeographicalArea.EUROPE, "18", "28", "36", "37", "41", "45")
_register("94", GeographicalArea.EUROPE, "2A", "2B")
_register(
    "44",
    GeographicalArea.EUROPE,
    "08",
    "10",
    "51",
    "52",
    "54",
    "55",
    "57",
    "67",
    "68",
    "88",
)
_register("32", GeographicalArea.EUROPE, "02", "59", "60", "62", "80")
_register("11", GeographicalArea.EUROPE, "75", "77", "78", "91", "92", "93", "94", "95")
_register("28", GeographicalArea.EUROPE, "14", "27", "50", "61", "76")
_register(
    "75",
    GeographicalArea.EUROPE,
    "16",
    "17",
    "19",
    "23",
    "24",
    "33",
    "40",
    "47",
    "64",
    "79",
    "86",
    "87",
)
_register(
    "76",
    GeographicalArea.EUROPE,
    "09",
    "11",
    "12",
    "30",
    "31",
    "32",
    "34",
    "46",
    "48",
    "65",
    "66",
    "81",
    "82",
)
_register("52", GeographicalArea.EUROPE, "44", "49", "53", "72", "85")
_register("93", GeographicalArea.EUROPE, "04", "05", "06", "13", "83", "84")
_register("01", GeographicalArea.AMERIQUE, "971")
_register("02", GeographicalArea.AMERIQUE, "972")
_register("03", GeographicalArea.AMERIQUE, "973")
_register("04", GeographicalArea.AFRIQUE, "974")
_register("06", GeographicalArea.AFRIQUE, "976")


def region_et_zone_pour_departement(departement: Department) -> RegionEtZone | None:
    return _DEPARTEMENT_VERS_REGION.get(departement.code)
