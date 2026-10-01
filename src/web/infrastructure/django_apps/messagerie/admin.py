from django.contrib import admin

from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageDocumentModel,
    MessageModel,
)
from infrastructure.django_apps.utils.admin import (
    ReadOnlyAdminMixin,
    ReadOnlyInlineMixin,
)


class MessageInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = MessageModel
    fk_name = "conversation"
    fields = ("auteur", "contenu", "created_at")
    extra = 0
    show_change_link = True


@admin.register(ConversationModel)
class ConversationAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("objet", "candidature", "created_at")
    list_select_related = ("candidature",)
    date_hierarchy = "created_at"
    inlines = (MessageInline,)


class MessageDocumentInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = MessageDocumentModel
    fk_name = "message"
    fields = ("document", "created_at")
    extra = 0
    show_change_link = True


@admin.register(MessageModel)
class MessageAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("conversation", "auteur", "created_at")
    list_select_related = ("conversation", "auteur")
    date_hierarchy = "created_at"
    inlines = (MessageDocumentInline,)
