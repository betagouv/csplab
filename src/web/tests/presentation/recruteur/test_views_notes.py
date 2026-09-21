from datetime import timedelta
from uuid import UUID

from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import status

from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory

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


class TestCandidatureNotesView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(NOTES_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_notes_newest_first_without_deleted_ones(
        self, authenticated_client
    ):
        candidature = CandidatureDjangoFactory(id=UUID(CANDIDATURE_UUID))
        older = NoteDjangoFactory(candidature=candidature, message="a")
        newer = NoteDjangoFactory(candidature=candidature, message="b")
        NoteDjangoFactory(
            candidature=candidature, message="supprimée", supprimee_le=timezone.now()
        )
        NoteModel.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )

        response = authenticated_client.get(NOTES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert [n["entity_id"] for n in response.json()] == [
            str(newer.id),
            str(older.id),
        ]

    def test_post_requires_message(self, authenticated_client):
        response = authenticated_client.post(NOTES_URL, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_unknown_candidature(self, authenticated_client, test_user):
        AgentDjangoFactory(utilisateur=test_user)

        response = authenticated_client.post(
            NOTES_URL, data={"message": "x"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

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


class TestCandidatureNoteDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert (
            api_client.delete(NOTE_DETAIL_URL).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

    def test_patch_requires_message(self, authenticated_client):
        response = authenticated_client.patch(NOTE_DETAIL_URL, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_unknown_note(self, authenticated_client):
        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "x"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_note_of_another_author(self, authenticated_client):
        NoteDjangoFactory(id=UUID(NOTE_UUID), message="avant")

        response = authenticated_client.patch(
            NOTE_DETAIL_URL, data={"message": "après"}, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteModel.objects.get(id=UUID(NOTE_UUID)).message == "avant"

    def test_delete_unknown_note(self, authenticated_client):
        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note_of_another_author(self, authenticated_client):
        NoteDjangoFactory(id=UUID(NOTE_UUID))

        response = authenticated_client.delete(NOTE_DETAIL_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteModel.objects.get(id=UUID(NOTE_UUID)).supprimee_le is None

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
