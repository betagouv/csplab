from django.contrib import admin

from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.corps import CorpsModel
from infrastructure.django_apps.shared.models.metier import MetierModel
from infrastructure.django_apps.shared.models.offer import OfferModel


@admin.register(OfferModel)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "verse",
        "title",
        "category",
        "contract_type",
        "region",
        "department",
        "beginning_date",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "verse",
        "category",
        "contract_type",
        "region",
        "created_at",
        "updated_at",
    )
    search_fields = ("external_id", "title", "profile", "mission", "organization")
    readonly_fields = [f.name for f in OfferModel._meta.get_fields()]


@admin.register(CorpsModel)
class CorpsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "short_label",
        "category",
        "ministry",
        "diploma_level",
        "access_modalities",
    )
    list_filter = ("category", "ministry", "diploma_level")
    search_fields = ("code", "short_label", "long_label")
    readonly_fields = [f.name for f in CorpsModel._meta.get_fields()]

    fieldsets = (
        (
            "Informations générales",
            {"fields": ("id", "code", "short_label", "long_label")},
        ),
        ("Classification", {"fields": ("category", "ministry", "diploma_level")}),
        ("Modalités d'accès", {"fields": ("access_modalities",)}),
        (
            "Métadonnées",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(ConcoursModel)
class ConcoursAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nor_original",
        "corps",
        "grade",
        "category",
        "ministry",
        "open_position_number",
        "written_exam_date",
    )
    list_filter = ("category", "ministry", "written_exam_date")
    search_fields = ("nor_original", "corps", "grade")
    readonly_fields = [f.name for f in ConcoursModel._meta.get_fields()]

    fieldsets = (
        (
            "Informations générales",
            {"fields": ("id", "nor_original", "corps", "grade")},
        ),
        ("Classification", {"fields": ("category", "ministry")}),
        ("Modalités d'accès", {"fields": ("access_modality",)}),
        (
            "Détails du concours",
            {"fields": ("open_position_number", "written_exam_date")},
        ),
        ("NOR associés", {"fields": ("nor_list",)}),
        (
            "Métadonnées",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(MetierModel)
class MetierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "code_emploi_csp",
        "libelle_long",
        "libelle_domaine_fonctionnel",
    )
    list_filter = ("referenciel_metier_id", "libelle_domaine_fonctionnel")
    search_fields = (
        "id",
        "external_id",
        "code_emploi_csp",
        "libelle_long",
        "libelle_domaine_fonctionnel",
    )
    readonly_fields = [f.name for f in MetierModel._meta.get_fields()]
