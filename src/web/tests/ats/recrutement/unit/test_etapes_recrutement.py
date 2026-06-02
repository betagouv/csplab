import pytest

from domain.recrutement.errors.erreur_recrutement import EtapeRecrutementInvalide
from domain.recrutement.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
    EtapesRecrutement,
)
from tests.ats.recrutement.factories.organisme_factory import (
    make_etape_recrutement,
    make_etapes_recrutement,
)


def test_ordonnees_retourne_etapes_par_rang_croissant():
    collection = make_etapes_recrutement()
    ordonnees = collection.ordonnees()
    rangs = [e.rang for e in ordonnees]
    assert rangs == sorted(rangs)
    assert len(rangs) == len(set(rangs))  # tous distincts


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
    with pytest.raises(EtapeRecrutementInvalide, match=match):
        EtapeRecrutement(
            rang=rang,
            identifiant=identifiant,
            categorie=CategorieEtapeRecrutement.RECEPTION,
            nom=nom,
        )


def test_etapes_recrutement_identifiants_en_doublon_raises() -> None:
    etape_1 = make_etape_recrutement(rang=1, identifiant="reception", nom="Réception")
    etape_2 = make_etape_recrutement(
        rang=2, identifiant="reception", nom="Réception bis"
    )
    with pytest.raises(EtapeRecrutementInvalide, match="identifiants en doublon"):
        EtapesRecrutement(etapes=(etape_1, etape_2))


def test_etape_recrutement_categorie_invalide_raises() -> None:
    with pytest.raises(
        EtapeRecrutementInvalide,
        match="categorie doit être une CategorieEtapeRecrutement valide",
    ):
        EtapeRecrutement(
            rang=1,
            identifiant="reception",
            categorie="n_importe_quoi",  # type: ignore[arg-type]
            nom="Réception",
        )
