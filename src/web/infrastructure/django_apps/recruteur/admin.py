from django import forms
from django.contrib import admin
from pydantic import ValidationError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.recruteur.services.create_organisme import create_organisme
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.django_apps.utils.admin import (
    ReadOnlyAdminMixin,
    ReadOnlyInlineMixin,
)
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
        choices=[("", "---------")]
        + [(code, name) for code, name in sorted(Region.NAMES.items())],
        required=False,
        label="Région",
        help_text="Obligatoire en France, vide pour un autre pays.",
    )
    department = forms.ChoiceField(
        choices=[("", "---------")]
        + [(code, name) for code, name in sorted(Department.NAMES.items())],
        required=False,
        label="Département",
        help_text="Obligatoire en France, vide pour un autre pays.",
    )

    class Meta:
        model = OrganismeModel
        fields = [
            "nom",
            "versant",
            "siret",
            "parent_id",
            "external_id",
            "referentiel",
            "millesime",
            "area",
            "country",
            "region",
            "department",
        ]

    def clean_siret(self):
        siret = self.cleaned_data["siret"]
        try:
            SIRET(code=siret)
        except ValidationError as e:
            raise forms.ValidationError(f"SIRET invalide : {siret}") from e
        return siret

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk is not None:
            return cleaned_data
        has_subdivision = (
            bool(cleaned_data.get("region")),
            bool(cleaned_data.get("department")),
        )
        if cleaned_data.get("country") == "FRA" and has_subdivision != (True, True):
            raise forms.ValidationError(
                "La région et le département sont obligatoires en France."
            )
        if cleaned_data.get("country") != "FRA" and has_subdivision != (False, False):
            raise forms.ValidationError(
                "La région et le département doivent être vides hors de France."
            )
        return cleaned_data


class OrganismeAgentInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = OrganismeAgentModel
    fk_name = "organisme"
    fields = ("agent", "role", "created_at")
    extra = 0


@admin.register(OrganismeModel)
class OrganismeAdmin(admin.ModelAdmin):
    form = CreateOrganismeAdminForm
    list_display = ("id", "nom", "versant", "siret")
    search_fields = ("nom", "siret")
    list_filter = ("versant",)
    readonly_fields = ("id",)
    inlines = (OrganismeAgentInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            localisation = Localisation(
                area=GeographicalArea(form.cleaned_data["area"]),
                country=Country(form.cleaned_data["country"]),
                region=(
                    Region(code=form.cleaned_data["region"])
                    if form.cleaned_data["region"]
                    else None
                ),
                department=(
                    Department(code=form.cleaned_data["department"])
                    if form.cleaned_data["department"]
                    else None
                ),
            )
            organisme = create_organisme(
                nom=form.cleaned_data["nom"],
                versant=Verse(form.cleaned_data["versant"]),
                siret=form.cleaned_data["siret"],
                localisation=localisation,
                parent_id=form.cleaned_data.get("parent_id"),
                utilisateur=request.user,
            )
            obj.id = organisme.id
        else:
            # enforce the entity invariants (mapper builds the aggregate) before saving
            OrganismeIdentiteMapper().to_domain(obj)
            super().save_model(request, obj, form, change)


@admin.register(NoteModel)
class NoteAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("candidature", "publie_par", "created_at", "supprimee_le")
    list_filter = ("created_at", "supprimee_le")
    date_hierarchy = "created_at"


class RecrutementAgentInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = RecrutementAgentModel
    fk_name = "recrutement"
    fields = ("agent", "role", "created_at")
    extra = 0


@admin.register(RecrutementModel)
class RecrutementAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("offre", "organisme", "created_at", "updated_at")
    date_hierarchy = "created_at"
    inlines = (RecrutementAgentInline,)


@admin.register(EtapeModel)
class EtapeAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "recrutement", "categorie", "nom")
    list_filter = ("categorie",)
    search_fields = ("nom",)
    date_hierarchy = "created_at"
