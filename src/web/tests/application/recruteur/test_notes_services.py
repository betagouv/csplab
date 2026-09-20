from datetime import timedelta
from uuid import uuid4

import pytest
from django.utils import timezone
from faker import Faker

from application.recruteur.services.create_note import create_note
from application.recruteur.services.delete_note import delete_note
from application.recruteur.services.list_notes import list_notes
from application.recruteur.services.update_note import update_note
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

fake = Faker("fr_FR")


def _logs(note_id):
    return PostgresAuditLogRepository().get_logs_for_ressource("Note", note_id)


class TestCreateNote:
    def test_create_note_persists_and_logs(self, db):
        agent = AgentDjangoFactory()
        candidature = CandidatureDjangoFactory()
        message = fake.sentence()

        note = create_note(
            candidature_id=candidature.id,
            publie_par_id=agent.utilisateur_id,
            message=message,
        )

        saved = NoteModel.objects.get(pk=note.id)
        assert saved.message == message
        assert saved.candidature_id == candidature.id
        assert saved.publie_par_id == agent.utilisateur_id
        assert saved.supprimee_le is None
        (log,) = _logs(note.id)
        assert log.event_name == "NoteAjoutee"
        assert str(log.utilisateur_id) == str(agent.utilisateur_id)

    def test_create_note_unknown_candidature(self, db):
        agent = AgentDjangoFactory()

        with pytest.raises(CandidatureInexistante):
            create_note(
                candidature_id=uuid4(),
                publie_par_id=agent.utilisateur_id,
                message="x",
            )

        assert not NoteModel.objects.exists()

    def test_create_note_unknown_agent(self, db):
        candidature = CandidatureDjangoFactory()

        with pytest.raises(ProfilAgentNexistePas):
            create_note(
                candidature_id=candidature.id, publie_par_id=uuid4(), message="x"
            )

        assert not NoteModel.objects.exists()


class TestUpdateNote:
    def test_update_note_persists_and_logs(self, db):
        note = NoteDjangoFactory(message="avant")

        edited = update_note(
            note_id=note.id,
            message="après",
            utilisateur_id=note.publie_par_id,
        )

        assert edited.message == "après"
        assert NoteModel.objects.get(pk=note.id).message == "après"
        (log,) = _logs(note.id)
        assert log.event_name == "NoteEditee"

    def test_update_note_unknown_note(self, db):
        with pytest.raises(NoteIntrouvable):
            update_note(note_id=uuid4(), message="x", utilisateur_id=uuid4())

    def test_update_note_of_another_author_is_not_found(self, db):
        note = NoteDjangoFactory(message="avant")
        other_agent = AgentDjangoFactory()

        with pytest.raises(NoteIntrouvable):
            update_note(
                note_id=note.id,
                message="après",
                utilisateur_id=other_agent.utilisateur_id,
            )

        assert NoteModel.objects.get(pk=note.id).message == "avant"
        assert not _logs(note.id)

    def test_update_note_soft_deleted_is_not_found(self, db):
        note = NoteDjangoFactory(supprimee_le=timezone.now())

        with pytest.raises(NoteIntrouvable):
            update_note(note_id=note.id, message="x", utilisateur_id=note.publie_par_id)


class TestDeleteNote:
    def test_delete_note_soft_deletes_and_logs(self, db):
        note = NoteDjangoFactory()

        delete_note(note_id=note.id, utilisateur_id=note.publie_par_id)

        assert NoteModel.objects.get(pk=note.id).supprimee_le is not None
        (log,) = _logs(note.id)
        assert log.event_name == "NoteSupprimee"

    def test_delete_note_unknown_note(self, db):
        with pytest.raises(NoteIntrouvable):
            delete_note(note_id=uuid4(), utilisateur_id=uuid4())

    def test_delete_note_of_another_author_is_not_found(self, db):
        note = NoteDjangoFactory()
        other_agent = AgentDjangoFactory()

        with pytest.raises(NoteIntrouvable):
            delete_note(note_id=note.id, utilisateur_id=other_agent.utilisateur_id)

        assert NoteModel.objects.get(pk=note.id).supprimee_le is None
        assert not _logs(note.id)

    def test_delete_note_twice_is_not_found(self, db):
        note = NoteDjangoFactory()
        delete_note(note_id=note.id, utilisateur_id=note.publie_par_id)

        with pytest.raises(NoteIntrouvable):
            delete_note(note_id=note.id, utilisateur_id=note.publie_par_id)


class TestListNotes:
    def test_returns_notes_newest_first(self, db):
        candidature = CandidatureDjangoFactory()
        older = NoteDjangoFactory(candidature=candidature)
        newer = NoteDjangoFactory(candidature=candidature)
        NoteModel.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )

        notes = list_notes(candidature_id=candidature.id)

        assert [note.pk for note in notes] == [newer.pk, older.pk]

    def test_ignores_soft_deleted_notes(self, db):
        candidature = CandidatureDjangoFactory()
        kept = NoteDjangoFactory(candidature=candidature)
        NoteDjangoFactory(candidature=candidature, supprimee_le=timezone.now())

        notes = list_notes(candidature_id=candidature.id)

        assert [note.pk for note in notes] == [kept.pk]

    def test_ignores_other_candidatures(self, db):
        candidature = CandidatureDjangoFactory()
        NoteDjangoFactory()

        notes = list_notes(candidature_id=candidature.id)

        assert list(notes) == []

    def test_loads_author_without_extra_queries(self, db, django_assert_num_queries):
        candidature = CandidatureDjangoFactory()
        notes = NoteDjangoFactory.create_batch(3, candidature=candidature)

        with django_assert_num_queries(1):
            author_ids = [
                note.publie_par.utilisateur.pk
                for note in list_notes(candidature_id=candidature.id)
            ]

        assert len(author_ids) == len(notes)
