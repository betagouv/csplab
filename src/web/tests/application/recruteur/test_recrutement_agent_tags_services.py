from unittest.mock import Mock, patch

import pytest
from django.db import OperationalError, connections

from application.recruteur.services.add_recrutement_agent_tag import (
    add_recrutement_agent_tag,
)
from application.recruteur.services.remove_recrutement_agent_tag import (
    remove_recrutement_agent_tag,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.tag.models import (
    RecrutementAgentTagModel,
    RecrutementAgentTagQuerySet,
    TagCategory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
)
from infrastructure.factories.tag.tag_django_factory import (
    RecrutementAgentTagDjangoFactory,
    TagDjangoFactory,
)


def _superviseur_et_membre():
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    membre = RecrutementAgentDjangoFactory(recrutement__organisme=organisme)
    return superviseur, membre


def _member_events(agent_id) -> list[str]:
    return list(
        AuditLogModel.objects.filter(
            ressource_kind="RecrutementAgent", ressource_id=agent_id
        ).values_list("event_name", flat=True)
    )


def _revoke_from_a_second_connection(membre_id):
    connexion = connections.create_connection("default")
    try:
        connexion.set_autocommit(True)
        with connexion.cursor() as cursor:
            cursor.execute("SET lock_timeout = '500ms'")
            cursor.execute(
                "UPDATE recrutement_agent SET date_revocation = now(), "
                "updated_at = now() WHERE id = %s",
                [str(membre_id)],
            )
        return "révoqué"
    except OperationalError as error:
        assert getattr(error.__cause__, "sqlstate", None) == "55P03"  # lock_timeout
        return "bloquée par le verrou"
    finally:
        connexion.close()


# transactional_db : `db` masquerait un select_for_update hors transaction.atomic()
def test_add_recrutement_agent_tag_locks_the_member(transactional_db):
    superviseur, membre = _superviseur_et_membre()
    tag = TagDjangoFactory(
        organisme=membre.recrutement.organisme, category=TagCategory.RECRUTEMENT_AGENT
    )
    resultat = {}

    original = RecrutementAgentTagQuerySet.poser

    def poser_avec_revocation_concurrente(self, *args, **kwargs):
        resultat["revocation"] = _revoke_from_a_second_connection(membre.pk)
        return original(self, *args, **kwargs)

    with patch.object(
        RecrutementAgentTagQuerySet, "poser", poser_avec_revocation_concurrente
    ):
        add_recrutement_agent_tag(
            organisme_id=membre.recrutement.organisme_id,
            recrutement_id=membre.recrutement_id,
            agent_id=membre.agent_id,
            tag_id=tag.id,
            utilisateur=superviseur.utilisateur,
        )

    membre.refresh_from_db()
    assert resultat == {"revocation": "bloquée par le verrou"}
    assert membre.date_revocation is None
    assert list(
        RecrutementAgentTagModel.objects.filter(recrutement_agent=membre).values_list(
            "tag_id", flat=True
        )
    ) == [tag.id]
    assert _member_events(membre.agent_id) == ["EtiquettePosee"]


def test_remove_recrutement_agent_tag_locks_the_member(transactional_db):
    superviseur, membre = _superviseur_et_membre()
    pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)
    resultat = {}

    original = RecrutementAgentTagQuerySet.by_agent_and_tag

    def by_agent_and_tag_avec_revocation_concurrente(self, *args, **kwargs):
        resultat["revocation"] = _revoke_from_a_second_connection(membre.pk)
        return original(self, *args, **kwargs)

    with patch.object(
        RecrutementAgentTagQuerySet,
        "by_agent_and_tag",
        by_agent_and_tag_avec_revocation_concurrente,
    ):
        remove_recrutement_agent_tag(
            organisme_id=membre.recrutement.organisme_id,
            recrutement_id=membre.recrutement_id,
            agent_id=membre.agent_id,
            tag_id=pose.tag_id,
            utilisateur=superviseur.utilisateur,
        )

    membre.refresh_from_db()
    assert resultat == {"revocation": "bloquée par le verrou"}
    assert membre.date_revocation is None
    assert not RecrutementAgentTagModel.objects.filter(pk=pose.pk).exists()
    assert _member_events(membre.agent_id) == ["EtiquetteRetiree"]


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_add_recrutement_agent_tag_rolls_back_when_audit_log_fails(db):
    superviseur, membre = _superviseur_et_membre()
    tag = TagDjangoFactory(
        organisme=membre.recrutement.organisme, category=TagCategory.RECRUTEMENT_AGENT
    )

    with pytest.raises(RuntimeError):
        add_recrutement_agent_tag(
            organisme_id=membre.recrutement.organisme_id,
            recrutement_id=membre.recrutement_id,
            agent_id=membre.agent_id,
            tag_id=tag.id,
            utilisateur=superviseur.utilisateur,
        )

    assert not RecrutementAgentTagModel.objects.filter(
        recrutement_agent=membre
    ).exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_remove_recrutement_agent_tag_rolls_back_when_audit_log_fails(db):
    superviseur, membre = _superviseur_et_membre()
    pose = RecrutementAgentTagDjangoFactory(recrutement_agent=membre)

    with pytest.raises(RuntimeError):
        remove_recrutement_agent_tag(
            organisme_id=membre.recrutement.organisme_id,
            recrutement_id=membre.recrutement_id,
            agent_id=membre.agent_id,
            tag_id=pose.tag_id,
            utilisateur=superviseur.utilisateur,
        )

    assert RecrutementAgentTagModel.objects.filter(pk=pose.pk).exists()
