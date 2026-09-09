from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.recruteur.usecases.creer_note import CreerNoteCommand
from application.recruteur.usecases.editer_note import EditerNoteCommand
from application.recruteur.usecases.supprimer_note import SupprimerNoteCommand
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.recruteur.note_factory import NoteFactory

fake = Faker()

CANDIDATURE_UUID = str(fake.uuid4())
NOTE_UUID = str(fake.uuid4())

NOTES_URL = reverse(
    "recruteur:candidature-notes",
    kwargs={"candidature_uuid": CANDIDATURE_UUID},
)
NOTE_DETAIL_URL = reverse(
    "recruteur:candidature-note-detail",
    # TODO supprimer candidature_id
    kwargs={"candidature_uuid": CANDIDATURE_UUID, "note_uuid": NOTE_UUID},
)


@pytest.fixture
def container():
    with patch("presentation.recruteur.views.notes.recruteur_container") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestCandidatureNotesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(NOTES_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_notes(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = [
            NoteFactory.create_read_model(message="a"),
            NoteFactory.create_read_model(message="b"),
        ]
        container.lister_notes_candidature_usecase.return_value = mock_usecase

        response = authenticated_client.get(NOTES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert [n["message"] for n in response.json()] == ["a", "b"]

    def test_create_note(self, container, authenticated_client, test_user):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = NoteFactory.create_entity(
            message="nouvelle note"
        )
        container.creer_note_usecase.return_value = mock_usecase

        response = authenticated_client.post(
            NOTES_URL, data={"message": "nouvelle note"}, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "nouvelle note"
        mock_usecase.execute.assert_called_once_with(
            CreerNoteCommand(
                candidature_id=UUID(CANDIDATURE_UUID),
                publie_par_id=test_user.username,
                message="nouvelle note",
            )
        )

    def test_create_note_requires_message(self, container, authenticated_client):
        container.creer_note_usecase.return_value = MagicMock()

        response = authenticated_client.post(NOTES_URL, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_note_unknown_candidature(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = CandidatureInexistante(uuid4())
        container.creer_note_usecase.return_value = mock_usecase

        response = authenticated_client.post(
            NOTES_URL, data={"message": "x"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestNoteDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert (
            api_client.delete(NOTE_DETAIL_URL).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

    def test_edit_note(self, container, authenticated_client, test_user):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = NoteFactory.create_entity(
            message="modifiée"
        )
        container.editer_note_usecase.return_value = mock_usecase

        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "modifiée"}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        mock_usecase.execute.assert_called_once_with(
            EditerNoteCommand(
                note_id=UUID(NOTE_UUID),
                message="modifiée",
                mis_a_jour_par_id=test_user.username,
            )
        )

    def test_edit_note_not_found(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = NoteIntrouvable(uuid4())
        container.editer_note_usecase.return_value = mock_usecase

        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "x"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note(self, container, authenticated_client, test_user):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = None
        container.supprimer_note_usecase.return_value = mock_usecase

        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_usecase.execute.assert_called_once_with(
            SupprimerNoteCommand(
                note_id=UUID(NOTE_UUID),
                supprime_par_id=test_user.username,
            )
        )

    def test_delete_note_not_found(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = NoteIntrouvable(uuid4())
        container.supprimer_note_usecase.return_value = mock_usecase

        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCandidatureNotesViewDbVerified:
    def test_returns_persisted_notes(self, authenticated_client):
        candidature = CandidatureDjangoFactory(id=UUID(CANDIDATURE_UUID))
        note = NoteDjangoFactory(candidature=candidature, message="Bon profil")

        response = authenticated_client.get(NOTES_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["entity_id"] == str(note.id)
        assert data[0]["message"] == "Bon profil"
        assert data[0]["publie_par_id"] == str(note.publie_par_id)
        assert data[0]["publie_par_prenom"] == note.publie_par.utilisateur.first_name
        assert data[0]["publie_par_nom"] == note.publie_par.utilisateur.last_name

    def test_post_creates_and_persists_the_note(self, authenticated_client, test_user):
        AgentDjangoFactory(utilisateur=test_user)
        CandidatureDjangoFactory(id=UUID(CANDIDATURE_UUID))

        response = authenticated_client.post(
            NOTES_URL, data={"message": "Nouvelle note"}, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["message"] == "Nouvelle note"
        assert data["candidature_id"] == CANDIDATURE_UUID
        assert data["publie_par_id"] == str(test_user.username)

        note = NoteModel.objects.get(id=data["entity_id"])
        assert note.message == "Nouvelle note"
        assert str(note.publie_par_id) == str(test_user.username)


class TestCandidatureNoteDetailViewDbVerified:
    def test_patch_updates_and_persists_the_note(self, authenticated_client, test_user):
        agent = AgentDjangoFactory(utilisateur=test_user)
        candidature = CandidatureDjangoFactory(id=UUID(CANDIDATURE_UUID))
        NoteDjangoFactory(id=UUID(NOTE_UUID), candidature=candidature, publie_par=agent)

        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "Message modifié"}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Message modifié"

        note = NoteModel.objects.get(id=UUID(NOTE_UUID))
        assert note.message == "Message modifié"

    def test_delete_removes_the_note(self, authenticated_client, test_user):
        agent = AgentDjangoFactory(utilisateur=test_user)
        candidature = CandidatureDjangoFactory(id=UUID(CANDIDATURE_UUID))
        NoteDjangoFactory(id=UUID(NOTE_UUID), candidature=candidature, publie_par=agent)

        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        note = NoteModel.objects.get(id=UUID(NOTE_UUID))
        assert note.supprimee_le is not None
