from dataclasses import dataclass
from typing import TypedDict


class RecrutementSpec(TypedDict):
    intitule: str
    archive_depuis_jours: int | None
    repartition: tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class SpecOrganisme:
    cle: str
    graine: int
    recrutements: list[RecrutementSpec]


# repartition : candidatures par étape, dans l'ordre des étapes du recrutement.
_DIJOP = SpecOrganisme(
    cle="dijop",
    graine=1945,
    recrutements=[
        {
            "intitule": "Secrétaire général(e)",
            "archive_depuis_jours": None,
            "repartition": (52, 19, 9, 5, 9, 0),
        },
        {
            "intitule": "Conseiller(ère) héritage",
            "archive_depuis_jours": None,
            "repartition": (0, 0, 0, 0, 0, 0),
        },
        {
            "intitule": "Chargé(e) de mission infrastructures",
            "archive_depuis_jours": None,
            "repartition": (2, 1, 1, 0, 1, 0),
        },
        {
            "intitule": "Conseiller(ère) juridique / affaires législatives",
            "archive_depuis_jours": None,
            "repartition": (37, 13, 7, 3, 7, 0),
        },
        {
            "intitule": "Conseiller(ère) finances et garanties de l’État",
            "archive_depuis_jours": None,
            "repartition": (2, 1, 1, 0, 1, 0),
        },
        {
            "intitule": "Conseiller(ère) sécurité et ordre public",
            "archive_depuis_jours": None,
            "repartition": (27, 10, 5, 2, 4, 0),
        },
        {
            "intitule": "Conseiller(ère) transports et mobilités",
            "archive_depuis_jours": None,
            "repartition": (18, 6, 3, 2, 3, 0),
        },
        {
            "intitule": "Chargé(e) de mission relations territoriales",
            "archive_depuis_jours": None,
            "repartition": (2, 1, 1, 0, 1, 0),
        },
        {
            "intitule": "Chargé(e) de mission relations territoriales",
            "archive_depuis_jours": 20,
            "repartition": (1, 0, 2, 1, 7, 1),
        },
        {
            "intitule": "Chargé(e) de mission transition écologique et sobriété",
            "archive_depuis_jours": 45,
            "repartition": (1, 0, 3, 1, 10, 1),
        },
        {
            "intitule": "Chargé(e) de mission accessibilité et Jeux paralympiques",
            "archive_depuis_jours": 90,
            "repartition": (2, 0, 3, 2, 11, 1),
        },
    ],
)

SPECS_DEMO: dict[str, SpecOrganisme] = {spec.cle: spec for spec in (_DIJOP,)}
