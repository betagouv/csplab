from django.contrib import admin

from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.corps import CorpsModel
from infrastructure.django_apps.shared.models.metier import MetierModel
from infrastructure.django_apps.shared.models.offer import OfferModel


@admin.register(OfferModel)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "external_id",
        "code_emploi_csp",
        "verse",
        "title",
        "category",
        "contract_type",
        "region",
        "department",
        "beginning_date",
        "processed_at",
        "archived_at",
    )
    list_filter = (
        "verse",
        "category",
        "contract_type",
        "region",
        "created_at",
        "updated_at",
        "processed_at",
        "archived_at",
    )
    search_fields = (
        "external_id",
        "title",
        "profile",
        "mission",
        "organization",
        "code_emploi_csp",
    )
    readonly_fields = [f.name for f in OfferModel._meta.get_fields()]


@admin.register(CorpsModel)
class CorpsAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "short_label",
        "category",
        "ministry",
        "diploma_level",
        "access_modalities",
        "processed_at",
        "archived_at",
    )
    list_filter = (
        "category",
        "ministry",
        "diploma_level",
        "processed_at",
        "archived_at",
    )
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
        "nor_original",
        "corps",
        "grade",
        "category",
        "ministry",
        "open_position_number",
        "written_exam_date",
        "processed_at",
        "archived_at",
    )
    list_filter = (
        "category",
        "ministry",
        "written_exam_date",
        "processed_at",
        "archived_at",
    )
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
        "external_id",
        "libelle_long",
        "domaine_fonctionnel_code",
        "offer_family_code",
        "processed_at",
        "archived_at",
    )
    list_filter = (
        "domaine_fonctionnel_code",
        "offer_family_code",
        "processed_at",
        "archived_at",
    )
    search_fields = (
        "id",
        "external_id",
        "libelle_long",
        "domaine_fonctionnel_code",
        "offer_family_code",
    )
    readonly_fields = [f.name for f in MetierModel._meta.get_fields()]
