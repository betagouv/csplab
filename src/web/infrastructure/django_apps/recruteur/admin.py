from django import forms
from django.contrib import admin
from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from domain.identite.value_objects.siret import SIRET
from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.django_apps.recruteur.models import OrganismeModel


class CreateOrganismeAdminForm(forms.ModelForm):
    class Meta:
        model = OrganismeModel
        fields = ["nom", "versant", "siret", "parent_id"]


@admin.register(OrganismeModel)
class OrganismeAdmin(admin.ModelAdmin):
    form = CreateOrganismeAdminForm
    list_display = ("id", "nom", "versant", "siret")
    search_fields = ("nom", "siret")
    list_filter = ("versant",)
    readonly_fields = ("id",)

    def save_model(self, request, obj, form, change):
        if not change:
            siret_raw = form.cleaned_data.get("siret")
            command = CreateOrganismeCommand(
                nom=form.cleaned_data["nom"],
                versant=Verse(form.cleaned_data["versant"]),
                localisation=None,
                siret=SIRET(siret_raw) if siret_raw else None,
                parent_id=form.cleaned_data.get("parent_id"),
            )
            container = create_identite_container()
            organisme = container.create_organisme_usecase().execute(command)
            obj.pk = organisme.entity_id
            obj.id = organisme.entity_id
        else:
            super().save_model(request, obj, form, change)
