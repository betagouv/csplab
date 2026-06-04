import pytest

from domain.recruteur.errors.erreur_recrutement import EtapeInvalide
from domain.recruteur.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
    EtapesRecrutement,
)
from tests.factories.recruteur.organisme_factory import (
    make_etape_recrutement,
)


@pytest.mark.parametrize(
    ("identifiant", "nom", "match"),
    [
        ("   ", "Réception", "identifiant ne peut pas être vide"),
        ("reception", "   ", "nom ne peut pas être vide"),
    ],
)
def test_etape_recrutement_invalide_raises(
    identifiant: str, nom: str, match: str
) -> None:
    with pytest.raises(EtapeInvalide, match=match):
        EtapeRecrutement(
            identifiant=identifiant,
            categorie=CategorieEtapeRecrutement.INITIALE,
            nom=nom,
        )


def test_etapes_recrutement_identifiants_en_doublon_raises() -> None:
    etape_1 = make_etape_recrutement(identifiant="entree", nom="Réception")
    etape_2 = make_etape_recrutement(identifiant="entree", nom="Réception bis")
    with pytest.raises(EtapeInvalide, match="identifiants en doublon"):
        EtapesRecrutement(etapes=(etape_1, etape_2))


def test_etape_recrutement_categorie_invalide_raises() -> None:
    with pytest.raises(
        EtapeInvalide,
        match="categorie doit être une CategorieEtapeRecrutement valide",
    ):
        EtapeRecrutement(
            identifiant="entree",
            categorie="n_importe_quoi",  # type: ignore[arg-type]
            nom="N'importe quel nom",
        )
