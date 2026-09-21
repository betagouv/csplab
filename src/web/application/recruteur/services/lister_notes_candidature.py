from uuid import UUID

from django.db.models import QuerySet

from infrastructure.django_apps.recruteur.models.note import NoteModel


def lister_notes_candidature(*, candidature_id: UUID) -> QuerySet[NoteModel]:
    # TODO RBAC : l'utilisateur a t il le droit de consulter la liste
    # des notes de cette candidature
    return NoteModel.objects.by_candidature(candidature_id)
