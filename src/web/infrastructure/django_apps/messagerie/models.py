from django.db import models

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class ConversationQuerySet(models.QuerySet):
    def by_candidature_and_id(
        self, candidature_id, conversation_id
    ) -> "ConversationQuerySet":
        return self.filter(candidature_id=candidature_id, pk=conversation_id)


class ConversationModel(BaseDatedModel):
    candidature = models.ForeignKey(
        CandidatureModel,
        on_delete=models.PROTECT,
        db_column="candidature_id",
        related_name="conversations",
    )
    objet = models.CharField(max_length=255)

    objects = ConversationQuerySet.as_manager()
    class Meta:
        db_table = "conversation"
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(objet=""), name="conversation_objet_non_vide"
            )
        ]

    def __str__(self) -> str:
        return self.objet


class MessageModel(BaseDatedModel):
    conversation = models.ForeignKey(
        ConversationModel,
        on_delete=models.PROTECT,
        related_name="messages",
    )
    contenu = models.TextField()
    auteur = models.ForeignKey(
        UserModel,
        to_field="username",
        on_delete=models.PROTECT,
        db_column="auteur_id",
        related_name="messages_rediges",
    )

    class Meta:
        db_table = "message"
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(contenu=""), name="message_contenu_non_vide"
            )
        ]
        indexes = [
            models.Index(
                fields=["conversation", "created_at"],
                name="message_conv_created_idx",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)


class MessageDocumentModel(BaseDatedModel):
    # coherence between candidature of the doc and candidature of the msg should
    # be checked by the service
    message = models.ForeignKey(
        MessageModel,
        on_delete=models.PROTECT,
        related_name="pieces_jointes",
    )
    document = models.OneToOneField(
        DocumentModel,
        on_delete=models.PROTECT,
        related_name="piece_jointe",
    )

    class Meta:
        db_table = "message_document"
        verbose_name = "Pièce jointe de message"
        verbose_name_plural = "Pièces jointes de message"

    def __str__(self) -> str:
        return f"{self.message_id} - {self.document_id}"


class ConversationLectureModel(BaseDatedModel):
    conversation = models.ForeignKey(
        ConversationModel,
        on_delete=models.CASCADE,
        related_name="lectures",
    )
    # CASCADE: read receipt disappears with its author
    utilisateur = models.ForeignKey(
        UserModel,
        to_field="username",
        on_delete=models.CASCADE,
        db_column="utilisateur_id",
        related_name="lectures_conversations",
    )
    read_at = models.DateTimeField()

    class Meta:
        db_table = "conversation_lecture"
        verbose_name = "Lecture de conversation"
        verbose_name_plural = "Lectures de conversation"
        constraints = [
            models.UniqueConstraint(
                fields=["conversation", "utilisateur"],
                name="conversation_lecture_unique",
            )
        ]

    def __str__(self) -> str:
        return f"{self.conversation_id} - {self.utilisateur_id}"
