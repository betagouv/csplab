import pytest

from domain.recrutement.errors.erreur_recrutement import RecrutementInvalide
from domain.recrutement.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
)
from tests.ats.recrutement.factories.organisme_factory import make_etapes_recrutement


def test_ordonnees_retourne_etapes_par_rang_croissant():
    collection = make_etapes_recrutement()
    ordonnees = collection.ordonnees()
    assert [e.rang for e in ordonnees] == [1, 2, 3, 4, 5, 6]


@pytest.mark.parametrize(
    ("rang", "identifiant", "nom", "match"),
    [
        (0, "reception", "Réception", "rang doit être un entier strictement positif"),
        (-1, "reception", "Réception", "rang doit être un entier strictement positif"),
        (1, "   ", "Réception", "identifiant ne peut pas être vide"),
        (1, "reception", "   ", "nom ne peut pas être vide"),
    ],
)
def test_etape_recrutement_invalide_raises(
    rang: int, identifiant: str, nom: str, match: str
) -> None:
    with pytest.raises(RecrutementInvalide, match=match):
        EtapeRecrutement(
            rang=rang,
            identifiant=identifiant,
            categorie=CategorieEtapeRecrutement.RECEPTION,
            nom=nom,
        )
