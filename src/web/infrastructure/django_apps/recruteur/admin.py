from django import forms
from django.contrib import admin
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from domain.identite.errors.organisme_errors import SiretInvalide
from domain.identite.value_objects.siret import SIRET
from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.django_apps.utils.admin import ReadOnlyAdminMixin
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper


class CreateOrganismeAdminForm(forms.ModelForm):
    area = forms.ChoiceField(
        choices=[(g.value, g.name) for g in GeographicalArea],
        initial=GeographicalArea.EUROPE.value,
        label="Zone géographique",
    )
    country = forms.CharField(
        initial="FRA",
        label="Pays (code ISO 3166-1 alpha-3)",
        help_text="Ex: FRA pour France",
    )
    region = forms.ChoiceField(
        choices=[(code, name) for code, name in sorted(Region.NAMES.items())],
        label="Région",
    )
    department = forms.ChoiceField(
        choices=[(code, name) for code, name in sorted(Department.NAMES.items())],
        label="Département",
    )

    class Meta:
        model = OrganismeModel
        fields = [
            "nom",
            "versant",
            "siret",
            "parent_id",
            "area",
            "country",
            "region",
            "department",
        ]

    def clean_siret(self):
        siret = self.cleaned_data["siret"]
        try:
            SIRET(siret)
        except SiretInvalide as e:
            raise forms.ValidationError(f"SIRET invalide : {siret}") from e
        return siret


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
            localisation = Localisation(
                area=GeographicalArea(form.cleaned_data["area"]),
                country=Country(form.cleaned_data["country"]),
                region=Region(code=form.cleaned_data["region"]),
                department=Department(code=form.cleaned_data["department"]),
            )
            command = CreateOrganismeCommand(
                nom=form.cleaned_data["nom"],
                versant=Verse(form.cleaned_data["versant"]),
                localisation=localisation,
                siret=SIRET(siret_raw),
                parent_id=form.cleaned_data.get("parent_id"),
            )
            container = create_identite_container()
            organisme = container.create_organisme_usecase().execute(command)
            obj.id = organisme.entity_id
            # Create the organisme model with localisation data
            obj.localisation = {
                "area": localisation.area.value,
                "country": str(localisation.country),
                "region": localisation.region.code,
                "department": localisation.department.code,
            }
        else:
            # enforce the entity invariants (mapper builds the aggregate) before saving
            OrganismeIdentiteMapper().to_domain(obj)
            super().save_model(request, obj, form, change)


@admin.register(NoteModel)
class NoteAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("candidature", "publie_par", "created_at", "supprimee_le")
    list_filter = ("created_at", "supprimee_le")
    date_hierarchy = "created_at"


@admin.register(RecrutementModel)
class RecrutementAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("offre", "organisme", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(EtapeModel)
class EtapeAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "recrutement", "categorie", "nom")
    list_filter = ("categorie",)
    search_fields = ("nom",)
    date_hierarchy = "created_at"


@admin.register(RecrutementAgentModel)
class RecrutementAgentModelAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("recrutement", "agent", "created_at")
    search_fields = (
        "recrutement__offre__reference",
        "agent__utilisateur__first_name",
        "agent__utilisateur__last_name",
    )
