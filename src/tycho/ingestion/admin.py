from django.contrib import admin

from ingestion.models import RawExamination

class RawExaminationAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('nor', 'legitext_id') # liste les champs que nous voulons sur l'affichage


admin.site.register(RawExamination, RawExaminationAdmin)
