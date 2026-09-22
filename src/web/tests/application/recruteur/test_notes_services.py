from datetime import timedelta
from uuid import uuid4

import pytest
from django.utils import timezone
from faker import Faker

from application.recruteur.services.create_note import create_note
from application.recruteur.services.delete_note import delete_note
from application.recruteur.services.list_notes import list_notes
from application.recruteur.services.update_note import update_note
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

fake = Faker("fr_FR")


def _utilisateur(entity_id, *, is_staff=False):
    return UtilisateurFactory.create_entity(entity_id=entity_id, is_staff=is_staff)


def _logs(note_id):
    return PostgresAuditLogRepository().get_logs_for_ressource("Note", note_id)


class TestListNotes:
    def test_returns_notes_newest_first(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        older = NoteDjangoFactory(candidature=candidature)
        newer = NoteDjangoFactory(candidature=candidature)
        NoteModel.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )

        notes = list_notes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert [note.pk for note in notes] == [newer.pk, older.pk]

    def test_ignores_soft_deleted_notes(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        kept = NoteDjangoFactory(candidature=candidature)
        NoteDjangoFactory(candidature=candidature, supprimee_le=timezone.now())

        notes = list_notes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert [note.pk for note in notes] == [kept.pk]

    def test_ignores_other_candidatures(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        NoteDjangoFactory()

        notes = list_notes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert list(notes) == []

    def test_loads_author_without_extra_queries(self, db, django_assert_num_queries):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        notes = NoteDjangoFactory.create_batch(3, candidature=candidature)

        result = list_notes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        with django_assert_num_queries(1):
            author_ids = [note.publie_par.utilisateur.pk for note in result]

        assert len(author_ids) == len(notes)

    def test_denied_without_organisme_role(self, db):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )

        with pytest.raises(AccesOrganismeRefuse):
            list_notes(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                utilisateur=_utilisateur(uuid4()),
            )

    def test_denied_when_agent_role_not_attached_to_recrutement(self, db):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)

        with pytest.raises(AccesRecrutementRefuse):
            list_notes(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                utilisateur=_utilisateur(membre.utilisateur_id),
            )

    def test_allowed_for_agent_role_attached_as_contributeur(self, db):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            agent_link__agent=membre,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
        note = NoteDjangoFactory(candidature=candidature)

        notes = list_notes(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            utilisateur=_utilisateur(membre.utilisateur_id),
        )

        assert [n.pk for n in notes] == [note.pk]

    def test_recrutement_not_in_organisme(self, db):
        agent, organisme, _recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        other_recrutement = RecrutementDjangoFactory()

        with pytest.raises(RecrutementInexistant):
            list_notes(
                organisme_id=organisme.id,
                recrutement_id=other_recrutement.pk,
                candidature_id=candidature.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_candidature_not_in_recrutement(self, db):
        agent, organisme, recrutement, _candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        other_candidature = CandidatureDjangoFactory()

        with pytest.raises(RecrutementCandidatureInexistante):
            list_notes(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=other_candidature.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

class TestCreateNote:
    def test_create_note_persists_and_logs(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        message = fake.sentence()

        note = create_note(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            message=message,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        saved = NoteModel.objects.get(pk=note.id)
        assert saved.message == message
        assert saved.candidature_id == candidature.id
        assert saved.publie_par_id == agent.utilisateur_id
        assert saved.supprimee_le is None
        (log,) = _logs(note.id)
        assert log.event_name == "NoteAjoutee"
        assert str(log.utilisateur_id) == str(agent.utilisateur_id)

    def test_denied_without_organisme_role(self, db):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )

        with pytest.raises(AccesOrganismeRefuse):
            create_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                message="x",
                utilisateur=_utilisateur(uuid4()),
            )

        assert not NoteModel.objects.exists()

    def test_recrutement_not_in_organisme(self, db):
        agent, organisme, _recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        other_recrutement = RecrutementDjangoFactory()

        with pytest.raises(RecrutementInexistant):
            create_note(
                organisme_id=organisme.id,
                recrutement_id=other_recrutement.pk,
                candidature_id=candidature.id,
                message="x",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

        assert not NoteModel.objects.exists()

    def test_candidature_not_in_recrutement(self, db):
        agent, organisme, recrutement, _candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        other_candidature = CandidatureDjangoFactory()

        with pytest.raises(RecrutementCandidatureInexistante):
            create_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=other_candidature.id,
                message="x",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

        assert not NoteModel.objects.exists()


class TestUpdateNote:
    def test_update_note_persists_and_logs(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, message="avant"
        )

        edited = update_note(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.id,
            note_id=note.id,
            message="après",
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert edited.message == "après"
        assert NoteModel.objects.get(pk=note.id).message == "après"
        (log,) = _logs(note.id)
        assert log.event_name == "NoteEditee"

    def test_update_note_unknown_note(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )

        with pytest.raises(NoteIntrouvable):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                note_id=uuid4(),
                message="x",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_update_note_of_another_author_is_not_found(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        note = NoteDjangoFactory(candidature=candidature, message="avant")

        with pytest.raises(NoteIntrouvable):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                note_id=note.id,
                message="après",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

        assert NoteModel.objects.get(pk=note.id).message == "avant"
        assert not _logs(note.id)

    def test_update_note_of_another_candidature_is_not_found(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        note = NoteDjangoFactory(publie_par=agent, message="avant")

        with pytest.raises(NoteIntrouvable):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                note_id=note.id,
                message="après",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

        assert NoteModel.objects.get(pk=note.id).message == "avant"
        assert not _logs(note.id)

    def test_update_note_soft_deleted_is_not_found(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, supprimee_le=timezone.now()
        )

        with pytest.raises(NoteIntrouvable):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                note_id=note.id,
                message="x",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_denied_without_organisme_role(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        with pytest.raises(AccesOrganismeRefuse):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                note_id=note.id,
                message="x",
                utilisateur=_utilisateur(uuid4()),
            )

        assert NoteModel.objects.get(pk=note.id).message == note.message

    def test_recrutement_not_in_organisme(self, db):
        agent, organisme, _recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        other_recrutement = RecrutementDjangoFactory()
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        with pytest.raises(RecrutementInexistant):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=other_recrutement.pk,
                candidature_id=candidature.id,
                note_id=note.id,
                message="x",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_candidature_not_in_recrutement(self, db):
        agent, organisme, recrutement, _candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        other_candidature = CandidatureDjangoFactory()
        note = NoteDjangoFactory(candidature=other_candidature, publie_par=agent)

        with pytest.raises(RecrutementCandidatureInexistante):
            update_note(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=other_candidature.id,
                note_id=note.id,
                message="x",
                utilisateur=_utilisateur(agent.utilisateur_id),
            )


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
