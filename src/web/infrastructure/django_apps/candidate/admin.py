from django.contrib import admin

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.utils.admin import ReadOnlyAdminMixin


@admin.register(CVMetadataModel)
class CVMetadataAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("filename", "id", "created_at", "search_query")
    list_filter = ("created_at",)
    search_fields = ("filename", "id")


@admin.register(CandidatureModel)
class CandidatureAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "candidat",
        "etape__categorie",
        "etape__recrutement",
        "created_at",
        "updated_at",
    )
    list_filter = ("statut",)
    search_fields = (
        "etape__recrutement__offre__reference",
        "candidat__utilisateur__first_name",
        "candidat__utilisateur__last_name",
    )
