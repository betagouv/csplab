from datetime import timedelta
from uuid import uuid4

import pytest
from django.utils import timezone
from faker import Faker

from application.recruteur.services.creer_note import creer_note
from application.recruteur.services.editer_note import editer_note
from application.recruteur.services.lister_notes_candidature import (
    lister_notes_candidature,
)
from application.recruteur.services.supprimer_note import supprimer_note
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


class TestCreerNote:
    def test_creer_note_persists_and_logs(self, db):
        agent = AgentDjangoFactory()
        candidature = CandidatureDjangoFactory()
        message = fake.sentence()

        note = creer_note(
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

    def test_creer_note_unknown_candidature(self, db):
        agent = AgentDjangoFactory()

        with pytest.raises(CandidatureInexistante):
            creer_note(
                candidature_id=uuid4(),
                publie_par_id=agent.utilisateur_id,
                message="x",
            )

        assert not NoteModel.objects.exists()

    def test_creer_note_unknown_agent(self, db):
        candidature = CandidatureDjangoFactory()

        with pytest.raises(ProfilAgentNexistePas):
            creer_note(
                candidature_id=candidature.id, publie_par_id=uuid4(), message="x"
            )

        assert not NoteModel.objects.exists()
