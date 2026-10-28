from uuid import uuid4

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from infrastructure.django_apps.tag.models import NoteTagModel, TagCategory
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.tag.tag_django_factory import (
    NoteTagDjangoFactory,
    TagDjangoFactory,
)


def _note_tags_url(organisme_id, recrutement_id, candidature_id, note_id) -> str:
    return reverse(
        "recruteur:candidature_note_tags",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
            "note_uuid": str(note_id),
        },
    )


def _note_tag_url(organisme_id, recrutement_id, candidature_id, note_id, tag_id) -> str:
    return reverse(
        "recruteur:candidature_note_tag",
        kwargs={
            "organisme_uuid": str(organisme_id),
            "recrutement_uuid": str(recrutement_id),
            "candidature_uuid": str(candidature_id),
            "note_uuid": str(note_id),
            "tag_uuid": str(tag_id),
        },
    )


class TestCandidatureNoteTagsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _note_tags_url(uuid4(), uuid4(), uuid4(), uuid4())

        response = api_client.post(url, data={"tag_uuid": str(uuid4())}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        note = NoteDjangoFactory(candidature=candidature)
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_requires_tag_uuid(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "tag_uuid" in response.json()

    def test_note_of_another_author_is_not_found(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature)
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not NoteTagModel.objects.filter(note=note).exists()

    def test_deleted_note_is_not_found(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, supprimee_le=timezone.now()
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not NoteTagModel.objects.filter(note=note).exists()

    def test_tag_of_another_organisme_is_not_found(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        tag = TagDjangoFactory(category=TagCategory.NOTE)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not NoteTagModel.objects.filter(note=note).exists()

    def test_tag_of_another_category_is_rejected(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "tag_uuid" in response.json()
        assert not NoteTagModel.objects.filter(note=note).exists()

    def test_tag_already_on_note_is_a_conflict(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        tag = NoteTagDjangoFactory(note=note).tag

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert NoteTagModel.objects.filter(note=note, tag=tag).count() == 1

    @pytest.mark.parametrize("est_privee", [False, True])
    def test_tags_my_note(self, authenticated_client, test_user, est_privee):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, est_privee=est_privee
        )
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)

        response = authenticated_client.post(
            _note_tags_url(organisme.id, recrutement.pk, candidature.id, note.id),
            data={"tag_uuid": str(tag.id)},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.content == b""
        assert list(
            NoteTagModel.objects.filter(note=note).values_list("tag_id", flat=True)
        ) == [tag.id]


class TestCandidatureNoteTagDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        url = _note_tag_url(uuid4(), uuid4(), uuid4(), uuid4(), uuid4())

        response = api_client.delete(url, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_caller_without_organisme_role_is_forbidden(
        self, authenticated_client, test_user
    ):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=None)
        )
        pose = NoteTagDjangoFactory(note__candidature=candidature)

        response = authenticated_client.delete(
            _note_tag_url(
                organisme.id, recrutement.pk, candidature.id, pose.note_id, pose.tag_id
            ),
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert NoteTagModel.objects.filter(pk=pose.pk).exists()

    def test_note_of_another_author_is_not_found(self, authenticated_client, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        pose = NoteTagDjangoFactory(note__candidature=candidature)

        response = authenticated_client.delete(
            _note_tag_url(
                organisme.id, recrutement.pk, candidature.id, pose.note_id, pose.tag_id
            ),
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteTagModel.objects.filter(pk=pose.pk).exists()

    def test_deleted_note_is_not_found(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(
            candidature=candidature, publie_par=agent, supprimee_le=timezone.now()
        )
        pose = NoteTagDjangoFactory(note=note)

        response = authenticated_client.delete(
            _note_tag_url(
                organisme.id, recrutement.pk, candidature.id, note.id, pose.tag_id
            ),
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert NoteTagModel.objects.filter(pk=pose.pk).exists()

    def test_tag_not_on_note_is_not_found(self, authenticated_client, test_user):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        tag = TagDjangoFactory(organisme=organisme, category=TagCategory.NOTE)

        response = authenticated_client.delete(
            _note_tag_url(
                organisme.id, recrutement.pk, candidature.id, note.id, tag.id
            ),
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_removes_only_this_tag_from_this_note(
        self, authenticated_client, test_user
    ):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(utilisateur=test_user)
        )
        note = NoteDjangoFactory(candidature=candidature, publie_par=agent)
        pose = NoteTagDjangoFactory(note=note)
        autre_etiquette = NoteTagDjangoFactory(note=note)
        autre_note = NoteTagDjangoFactory(
            tag=pose.tag, note=NoteDjangoFactory(candidature=candidature)
        )

        response = authenticated_client.delete(
            _note_tag_url(
                organisme.id, recrutement.pk, candidature.id, note.id, pose.tag_id
            ),
            format="json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert set(NoteTagModel.objects.values_list("pk", flat=True)) == {
            autre_etiquette.pk,
            autre_note.pk,
        }
