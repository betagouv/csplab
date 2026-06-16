from django.contrib import admin

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from infrastructure.di.candidate.candidate_factory import create_candidate_container
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


@admin.register(CVMetadataModel)
class CVMetadataAdmin(admin.ModelAdmin):
    list_display = ("filename", "id", "created_at", "search_query")
    list_filter = ("created_at",)
    search_fields = ("filename", "id")
    readonly_fields = [f.name for f in CVMetadataModel._meta.get_fields()]


@admin.register(CandidatureModel)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "candidat_id",
        "offre_id",
        "statut",
        "created_at",
        "updated_at",
    )
    list_filter = ("statut",)
    search_fields = ("candidat_id", "offre_id")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("id", "candidat_id", "offre_id", "created_at", "updated_at")
        return ("id", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not change:
            command = SubmitApplicationCommand(
                offre_id=obj.offre_id,
                candidat_id=obj.candidat_id,
            )
            container = create_candidate_container()
            candidature = container.submit_application_usecase().execute(command)
            saved = CandidatureModel.from_entity(candidature)
            # Sync obj avec les valeurs du usecase
            obj.id = saved.id
            obj.statut = saved.statut
            # Forcer UPDATE (pas INSERT) car le usecase a déjà créé l'enregistrement
            obj._state.adding = False
        super().save_model(request, obj, form, change)
