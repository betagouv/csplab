from django.core.files.storage import storages
from django.db import models

from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.django_apps.utils.models import BaseDatedModel


def candidature_documents_storage():
    return storages["candidature_documents"]


def document_upload_to(instance: "DocumentModel", filename: str) -> str:
    return f"candidatures/{instance.candidature_id}/documents/{instance.id}"


class DocumentQuerySet(models.QuerySet):
    def by_recrutement_candidature_and_document(
        self, recrutement_id, candidature_id, document_id
    ) -> "DocumentQuerySet":
        return self.filter(
            candidature_id=candidature_id,
            candidature__etape__recrutement_id=recrutement_id,
            pk=document_id,
        )

    def by_recrutement_and_candidature(
        self, recrutement_id, candidature_id
    ) -> "DocumentQuerySet":
        return (
            self.select_related("depose_par")
            .filter(
                candidature_id=candidature_id,
                candidature__etape__recrutement_id=recrutement_id,
            )
            .order_by("-created_at")
        )


class DocumentModel(BaseDatedModel):
    candidature = models.ForeignKey(
        CandidatureModel,
        on_delete=models.PROTECT,
        db_column="candidature_id",
        # TODO: rename to related_name="documents" once the dead
        # CandidatureModel.documents JSONField is removed (see Step 6) — until
        # then it clashes with that field name (fields.E302/E303).
        related_name="documents_uploaded",
    )
    type_document = models.CharField(max_length=30, choices=TypeDocument.choices)
    fichier = models.FileField(
        storage=candidature_documents_storage,
        upload_to=document_upload_to,
        max_length=512,
    )
    nom_original = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    taille = models.PositiveIntegerField()
    depose_par = models.ForeignKey(
        UserModel,
        to_field="username",
        on_delete=models.PROTECT,
        db_column="depose_par_id",
        related_name="documents_deposes",
    )

    objects = DocumentQuerySet.as_manager()

    class Meta:
        db_table = "candidature_document"
        verbose_name = "Document de candidature"
        verbose_name_plural = "Documents de candidature"

    def __str__(self) -> str:
        return f"{self.type_document} - {self.id}"
