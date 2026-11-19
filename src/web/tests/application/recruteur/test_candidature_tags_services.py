from unittest.mock import patch

from django.db import OperationalError, connections

from application.recruteur.services.add_candidature_tag import add_candidature_tag
from application.recruteur.services.remove_candidature_tag import (
    remove_candidature_tag,
)
from infrastructure.django_apps.tag.models import (
    CandidatureTagModel,
    CandidatureTagQuerySet,
    TagCategory,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    TagDjangoFactory,
)


# transactional_db : `db` masquerait un select_for_update hors transaction.atomic()
def test_add_candidature_tag_runs_in_its_own_transaction(transactional_db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

    add_candidature_tag(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.id,
        tag_id=tag.id,
        utilisateur=agent.utilisateur,
    )

    assert list(
        CandidatureTagModel.objects.filter(candidature=candidature).values_list(
            "tag_id", flat=True
        )
    ) == [tag.id]


def _update_from_a_second_connection(sql, row_id):
    connexion = connections.create_connection("default")
    try:
        connexion.set_autocommit(True)
        with connexion.cursor() as cursor:
            cursor.execute("SET lock_timeout = '500ms'")
            cursor.execute(sql, [str(row_id)])
        return "modifiée"
    except OperationalError as error:
        assert getattr(error.__cause__, "sqlstate", None) == "55P03"  # lock_timeout
        return "bloquée par le verrou"
    finally:
        connexion.close()


def test_remove_candidature_tag_locks_the_candidature_not_its_etape(
    transactional_db,
):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    pose = CandidatureTagDjangoFactory(candidature=candidature)
    resultat = {}

    original = CandidatureTagQuerySet.by_candidature_and_tag

    def by_candidature_and_tag_avec_ecritures_concurrentes(self, *args, **kwargs):
        resultat["candidature"] = _update_from_a_second_connection(
            "UPDATE candidature SET updated_at = now() WHERE id = %s", candidature.id
        )
        resultat["etape"] = _update_from_a_second_connection(
            "UPDATE etape_recrutement SET updated_at = now() WHERE id = %s",
            candidature.etape_id,
        )
        return original(self, *args, **kwargs)

    with patch.object(
        CandidatureTagQuerySet,
        "by_candidature_and_tag",
        by_candidature_and_tag_avec_ecritures_concurrentes,
    ):
        remove_candidature_tag(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            tag_id=pose.tag_id,
            utilisateur=agent.utilisateur,
        )

    assert resultat == {"candidature": "bloquée par le verrou", "etape": "modifiée"}
    assert not CandidatureTagModel.objects.filter(pk=pose.pk).exists()
