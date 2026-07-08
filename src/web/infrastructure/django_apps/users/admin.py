from django.contrib import admin

from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
    ProfilCandidatModel,
    UserModel,
)
from infrastructure.django_apps.utils.admin import ReadOnlyAdminMixin


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "date_joined",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("email",)
    readonly_fields = ["username", "id", "date_joined", "last_login", "password"]
    filter_horizontal = ("sources",)


@admin.register(ProfilCandidatModel)
class ProfilCandidatAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("utilisateur", "created_at", "updated_at")
    search_fields = ("utilisateur__email",)
    date_hierarchy = "created_at"


@admin.register(ProfilAgentModel)
class ProfilAgentAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("utilisateur", "intitule_poste", "created_at", "updated_at")
    search_fields = ("utilisateur__email", "intitule_poste")
    date_hierarchy = "created_at"
