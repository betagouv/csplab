import pytest

from application.recruteur.context_services.etape_actions import (
    authorized_actions_of_etapes,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement as Categorie,
)

EN_COURS_ACTIONS = [
    "edit_etape",
    "delete_etape",
    "insert_etape_before",
    "insert_etape_after",
]


def test_each_categorie_gets_its_own_actions():
    categories = [
        Categorie.ENTREE,
        Categorie.EN_COURS,
        Categorie.EN_COURS,
        Categorie.REFUS,
        Categorie.ACCEPTE,
    ]

    assert authorized_actions_of_etapes(categories, can_update=True) == [
        ["insert_etape_after"],
        EN_COURS_ACTIONS,
        EN_COURS_ACTIONS,
        ["insert_etape_before"],
        [],
    ]


def test_the_only_en_cours_etape_cannot_be_deleted():
    categories = [
        Categorie.ENTREE,
        Categorie.EN_COURS,
        Categorie.REFUS,
        Categorie.ACCEPTE,
    ]

    assert authorized_actions_of_etapes(categories, can_update=True)[1] == [
        "edit_etape",
        "insert_etape_before",
        "insert_etape_after",
    ]


@pytest.mark.parametrize("nb_en_cours", [1, 3])
def test_without_the_right_to_modify_no_etape_has_actions(nb_en_cours):
    categories = [
        Categorie.ENTREE,
        *[Categorie.EN_COURS] * nb_en_cours,
        Categorie.REFUS,
        Categorie.ACCEPTE,
    ]

    assert authorized_actions_of_etapes(categories, can_update=False) == [
        [] for _ in categories
    ]
