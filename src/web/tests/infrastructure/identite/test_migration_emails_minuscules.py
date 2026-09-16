from importlib import import_module

import pytest
from django.db import migrations

from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

migration = import_module(
    "infrastructure.django_apps.users.migrations.0009_emails_en_minuscules"
)


# Double de la portion d'API de queryset utilisee par la migration.
#
# La detection de collision ne peut pas etre exercee sur la vraie base : celle
# des tests porte deja la contrainte ajoutee en 0010, qui rend impossible l'etat
# que la migration est censee rencontrer. En production 0009 s'execute avant
# 0010, donc avant la contrainte. Le double reproduit cet instant.
#
# Le dernier test du fichier verifie le comportement reel sur PostgreSQL, pour
# que ce double ne puisse pas s'ecarter de l'original sans qu'on le voie.
class FauxUserModel:
    def __init__(self, lignes: dict):
        self.lignes = dict(lignes)
        self.objects = self

    def values_list(self, *champs):
        assert champs == ("pk", "email")
        return list(self.lignes.items())

    def filter(self, pk):
        self._pk = pk
        return self

    def update(self, email):
        self.lignes[self._pk] = email
        return 1


class TestTrouverLesCollisions:
    def test_aucune_collision_sur_des_emails_distincts(self):
        faux = FauxUserModel({1: "a@gouv.fr", 2: "b@gouv.fr"})

        assert migration.trouver_les_collisions(faux) == {}

    def test_detecte_deux_comptes_qui_ne_different_que_par_la_casse(self):
        faux = FauxUserModel({1: "jean@gouv.fr", 2: "JEAN@GOUV.FR"})

        assert migration.trouver_les_collisions(faux) == {"jean@gouv.fr": [1, 2]}

    def test_detecte_aussi_une_collision_due_aux_espaces(self):
        faux = FauxUserModel({1: "jean@gouv.fr", 2: "  jean@gouv.fr  "})

        assert migration.trouver_les_collisions(faux) == {"jean@gouv.fr": [1, 2]}


class TestNormaliserLesEmails:
    def test_met_en_minuscules_et_retire_les_espaces(self):
        faux = FauxUserModel({1: "  Jean.DUPONT@GOUV.FR  "})

        modifies = migration.normaliser_les_emails(faux)

        assert faux.lignes[1] == "jean.dupont@gouv.fr"
        assert modifies == 1

    def test_ne_touche_pas_aux_emails_deja_normalises(self):
        faux = FauxUserModel({1: "deja@gouv.fr"})

        assert migration.normaliser_les_emails(faux) == 0
        assert faux.lignes[1] == "deja@gouv.fr"

    def test_s_interrompt_sur_une_collision_sans_rien_modifier(self):
        faux = FauxUserModel({1: "jean@gouv.fr", 2: "JEAN@GOUV.FR", 3: "  X@GOUV.FR "})

        with pytest.raises(RuntimeError, match="ne different que par la casse"):
            migration.normaliser_les_emails(faux)

        # Aucune ecriture, pas meme sur la ligne 3 qui n'est pas en cause.
        assert faux.lignes == {
            1: "jean@gouv.fr",
            2: "JEAN@GOUV.FR",
            3: "  X@GOUV.FR ",
        }

    def test_le_message_d_erreur_nomme_les_comptes_concernes(self):
        faux = FauxUserModel({7: "jean@gouv.fr", 9: "JEAN@GOUV.FR"})

        with pytest.raises(RuntimeError) as erreur:
            migration.normaliser_les_emails(faux)

        assert "jean@gouv.fr" in str(erreur.value)
        assert "[7, 9]" in str(erreur.value)


def test_le_retour_arriere_est_un_noop_assume():
    # Sans reverse_code, la migration serait irreversible et bloquerait tout
    # retour arriere de la base. Le noop est un choix, pas un oubli.
    operation = migration.Migration.operations[0]

    assert operation.reverse_code is migrations.RunPython.noop


def test_sur_postgresql_la_normalisation_corrige_bien_la_ligne(db):
    # Garde-fou : le double ci-dessus ne doit pas diverger du vrai modele.
    user = UtilisateurDjangoFactory(email="initial@gouv.fr")
    UserModel.objects.filter(pk=user.pk).update(email="  Jean.DUPONT@GOUV.FR  ")

    modifies = migration.normaliser_les_emails(UserModel)

    user.refresh_from_db()
    assert user.email == "jean.dupont@gouv.fr"
    assert modifies == 1
