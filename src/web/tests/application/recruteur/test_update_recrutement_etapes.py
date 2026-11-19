from unittest.mock import Mock, patch

import pytest
from django.db import OperationalError, connections

from application.recruteur.services.update_recrutement_etapes import (
    update_recrutement_etapes,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)


def _recrutement_avec_quatre_etapes():
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme, etapes=[])
    reception = EtapeDjangoFactory(
        recrutement=recrutement, nom="Réception", categorie="entree"
    )
    entretien = EtapeDjangoFactory(
        recrutement=recrutement, nom="Entretien", categorie="en_cours"
    )
    second = EtapeDjangoFactory(
        recrutement=recrutement, nom="Second", categorie="en_cours"
    )
    refus = EtapeDjangoFactory(recrutement=recrutement, nom="Refus", categorie="refus")
    recrutement.ordre_etapes = [
        str(etape.id) for etape in (reception, entretien, second, refus)
    ]
    recrutement.save(update_fields=["ordre_etapes"])
    return superviseur.utilisateur, organisme, recrutement, reception, entretien, refus


def _renomme_supprime_et_ajoute(reception, entretien, refus):
    return [
        EtapeData(
            etape_uuid=reception.id,
            nom="Accueil",
            categorie=CategorieEtapeRecrutement.ENTREE,
        ),
        EtapeData(
            etape_uuid=entretien.id,
            nom=entretien.nom,
            categorie=CategorieEtapeRecrutement.EN_COURS,
        ),
        EtapeData(
            etape_uuid=refus.id,
            nom=refus.nom,
            categorie=CategorieEtapeRecrutement.REFUS,
        ),
        EtapeData(
            etape_uuid=None,
            nom="Recrutement",
            categorie=CategorieEtapeRecrutement.ACCEPTE,
        ),
    ]


def _assert_etapes_inchangees(recrutement, ordre_avant, noms_avant):
    recrutement.refresh_from_db()
    assert recrutement.ordre_etapes == ordre_avant
    assert {etape.id: etape.nom for etape in EtapeModel.objects.all()} == noms_avant
    assert not AuditLogModel.objects.exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=[None, None, None, RuntimeError("audit log write failed")]),
)
def test_rolls_back_every_write_when_the_last_audit_log_fails(db):
    utilisateur, organisme, recrutement, reception, entretien, refus = (
        _recrutement_avec_quatre_etapes()
    )
    ordre_avant = list(recrutement.ordre_etapes)
    noms_avant = {etape.id: etape.nom for etape in EtapeModel.objects.all()}

    with pytest.raises(RuntimeError):
        update_recrutement_etapes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=utilisateur,
            etapes=_renomme_supprime_et_ajoute(reception, entretien, refus),
        )

    _assert_etapes_inchangees(recrutement, ordre_avant, noms_avant)


def test_rolls_back_every_write_when_saving_the_recrutement_fails(db):
    utilisateur, organisme, recrutement, reception, entretien, refus = (
        _recrutement_avec_quatre_etapes()
    )
    ordre_avant = list(recrutement.ordre_etapes)
    noms_avant = {etape.id: etape.nom for etape in EtapeModel.objects.all()}

    with (
        patch.object(RecrutementModel, "save", side_effect=RuntimeError("save failed")),
        pytest.raises(RuntimeError),
    ):
        update_recrutement_etapes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=utilisateur,
            etapes=_renomme_supprime_et_ajoute(reception, entretien, refus),
        )

    _assert_etapes_inchangees(recrutement, ordre_avant, noms_avant)


def _maj_concurrente_depuis_une_seconde_connexion(recrutement_id):
    meta = RecrutementModel._meta
    connexion = connections.create_connection("default")
    try:
        connexion.set_autocommit(True)
        with connexion.cursor() as cursor:
            cursor.execute("SET lock_timeout = '500ms'")
            cursor.execute(
                f"UPDATE {meta.db_table} SET updated_at = now()"  # noqa: S608
                f" WHERE {meta.pk.column} = %s",
                [str(recrutement_id)],
            )
        return "mise à jour"
    except OperationalError as error:
        assert getattr(error.__cause__, "sqlstate", None) == "55P03"  # lock_timeout
        return "bloquée par le verrou"
    finally:
        connexion.close()


# transactional_db : la seconde connexion doit voir des données commitées.
# La tentative part juste avant l'écriture du recrutement : seul le verrou du
# select_for_update tient la ligne à ce moment.
def test_locks_the_recrutement_against_a_concurrent_update(transactional_db):
    utilisateur, organisme, recrutement, reception, entretien, refus = (
        _recrutement_avec_quatre_etapes()
    )
    resultat = {}
    enregistrer = RecrutementModel.save

    def save_avec_maj_concurrente(self, *args, **kwargs):
        resultat["maj"] = _maj_concurrente_depuis_une_seconde_connexion(self.pk)
        return enregistrer(self, *args, **kwargs)

    with patch.object(RecrutementModel, "save", save_avec_maj_concurrente):
        update_recrutement_etapes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=utilisateur,
            etapes=_renomme_supprime_et_ajoute(reception, entretien, refus),
        )

    assert resultat == {"maj": "bloquée par le verrou"}
    assert EtapeModel.objects.get(pk=reception.pk).nom == "Accueil"
