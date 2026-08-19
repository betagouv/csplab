from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region

RegionEtZone = tuple[Region, GeographicalArea]

_DEPARTEMENT_VERS_REGION_ET_ZONE: dict[str, RegionEtZone] = {}


def _register(
    region: Region, area: GeographicalArea, *departements: Department
) -> None:
    for departement in departements:
        _DEPARTEMENT_VERS_REGION_ET_ZONE[departement.code] = (region, area)


def _departements(*codes: str) -> tuple[Department, ...]:
    return tuple(Department(code=code) for code in codes)


_register(
    Region(code="84"),
    GeographicalArea.EUROPE,
    *_departements(
        "01", "03", "07", "15", "26", "38", "42", "43", "63", "69", "73", "74"
    ),
)
_register(
    Region(code="27"),
    GeographicalArea.EUROPE,
    *_departements("21", "25", "39", "58", "70", "71", "89", "90"),
)
_register(
    Region(code="53"),
    GeographicalArea.EUROPE,
    *_departements("22", "29", "35", "56"),
)
_register(
    Region(code="24"),
    GeographicalArea.EUROPE,
    *_departements("18", "28", "36", "37", "41", "45"),
)
_register(
    Region(code="94"),
    GeographicalArea.EUROPE,
    *_departements("2A", "2B"),
)
_register(
    Region(code="44"),
    GeographicalArea.EUROPE,
    *_departements("08", "10", "51", "52", "54", "55", "57", "67", "68", "88"),
)
_register(
    Region(code="32"),
    GeographicalArea.EUROPE,
    *_departements("02", "59", "60", "62", "80"),
)
_register(
    Region(code="11"),
    GeographicalArea.EUROPE,
    *_departements("75", "77", "78", "91", "92", "93", "94", "95"),
)
_register(
    Region(code="28"),
    GeographicalArea.EUROPE,
    *_departements("14", "27", "50", "61", "76"),
)
_register(
    Region(code="75"),
    GeographicalArea.EUROPE,
    *_departements(
        "16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"
    ),
)
_register(
    Region(code="76"),
    GeographicalArea.EUROPE,
    *_departements(
        "09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"
    ),
)
_register(
    Region(code="52"),
    GeographicalArea.EUROPE,
    *_departements("44", "49", "53", "72", "85"),
)
_register(
    Region(code="93"),
    GeographicalArea.EUROPE,
    *_departements("04", "05", "06", "13", "83", "84"),
)
_register(Region(code="01"), GeographicalArea.AMERIQUE, *_departements("971"))
_register(Region(code="02"), GeographicalArea.AMERIQUE, *_departements("972"))
_register(Region(code="03"), GeographicalArea.AMERIQUE, *_departements("973"))
_register(Region(code="04"), GeographicalArea.AFRIQUE, *_departements("974"))
_register(Region(code="06"), GeographicalArea.AFRIQUE, *_departements("976"))


def region_et_zone_pour_departement(departement: Department) -> RegionEtZone | None:
    return _DEPARTEMENT_VERS_REGION_ET_ZONE.get(departement.code)
