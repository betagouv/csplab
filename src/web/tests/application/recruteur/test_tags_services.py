from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from django.db import OperationalError, connections
from django.db.models.sql.subqueries import DeleteQuery

from application.recruteur.services.create_tag import create_tag
from application.recruteur.services.delete_tag import delete_tag
from application.recruteur.services.remove_note_tag import remove_note_tag
from application.recruteur.services.update_tag import update_tag
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.tag.models import (
    CandidatureTagModel,
    NoteTagModel,
    TagCategory,
    TagColor,
    TagModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    NoteTagDjangoFactory,
    TagDjangoFactory,
)


@pytest.fixture(name="superviseur")
def superviseur_fixture(db):
    return create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_when_audit_log_fails(superviseur):
    agent, organisme = superviseur

    with pytest.raises(RuntimeError):
        create_tag(
            organisme_id=organisme.id,
            utilisateur=agent.utilisateur,
            name="Expert",
            category=TagCategory.CANDIDATURE,
        )

    assert not TagModel.objects.exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_update_rolls_back_when_audit_log_fails(superviseur):
    agent, organisme = superviseur
    tag = TagDjangoFactory(organisme=organisme, name="Expert")

    with pytest.raises(RuntimeError):
        update_tag(
            organisme_id=organisme.id,
            tag_id=tag.id,
            utilisateur=agent.utilisateur,
            name="Bon profil",
            color=TagColor.BLEU,
        )

    tag.refresh_from_db()
    assert tag.name == "Expert"


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_delete_rolls_back_when_audit_log_fails(superviseur):
    agent, organisme = superviseur
    tag = TagDjangoFactory(organisme=organisme)
    CandidatureTagDjangoFactory(tag=tag)

    with pytest.raises(RuntimeError):
        delete_tag(
            organisme_id=organisme.id, tag_id=tag.id, utilisateur=agent.utilisateur
        )

    assert TagModel.objects.filter(pk=tag.pk).exists()
    assert CandidatureTagModel.objects.filter(tag=tag).exists()


# transactional_db : le fixture `db` ouvre une transaction autour du test, qui
# masquerait un select_for_update appelé hors de transaction.atomic()
def test_remove_note_tag_runs_in_its_own_transaction(transactional_db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    pose = NoteTagDjangoFactory(note__candidature=candidature, note__publie_par=agent)

    remove_note_tag(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.id,
        note_id=pose.note_id,
        tag_id=pose.tag_id,
        utilisateur=agent.utilisateur,
    )

    assert not NoteTagModel.objects.filter(pk=pose.pk).exists()


def _concurrent_pose_from_a_second_connection(note_id, tag_id):
    connexion = connections.create_connection("default")
    try:
        connexion.set_autocommit(True)
        with connexion.cursor() as cursor:
            cursor.execute("SET lock_timeout = '500ms'")
            cursor.execute(
                "INSERT INTO note_tag (id, note_id, tag_id, created_at, updated_at)"
                " VALUES (%s, %s, %s, now(), now())",
                [str(uuid4()), str(note_id), str(tag_id)],
            )
        return "posée"
    except OperationalError as error:
        assert getattr(error.__cause__, "sqlstate", None) == "55P03"  # lock_timeout
        return "bloquée par le verrou"
    finally:
        connexion.close()


# Course du ticket #2170 : une pose commitée pendant la suppression de l'étiquette.
def test_delete_tag_locks_the_tag_against_a_concurrent_pose(transactional_db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)
    NoteTagDjangoFactory(tag=tag)
    note_concurrente = NoteDjangoFactory()
    resultat = {}

    original = DeleteQuery.delete_batch

    def delete_batch_avec_pose_concurrente(self, pk_list, using):
        if self.model is TagModel:
            resultat["pose"] = _concurrent_pose_from_a_second_connection(
                note_concurrente.pk, tag.pk
            )
        return original(self, pk_list, using)

    with patch.object(DeleteQuery, "delete_batch", delete_batch_avec_pose_concurrente):
        delete_tag(
            organisme_id=organisme.id, tag_id=tag.id, utilisateur=agent.utilisateur
        )

    assert resultat == {"pose": "bloquée par le verrou"}
    assert not TagModel.objects.filter(pk=tag.pk).exists()
    assert not NoteTagModel.objects.exists()
