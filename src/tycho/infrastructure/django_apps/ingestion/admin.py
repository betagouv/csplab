"""Django admin configuration for ingestion models."""

from django.contrib import admin

from infrastructure.django_apps.ingestion.models import RawDocument
from infrastructure.django_apps.shared.models import vectorized_document
from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.django_apps.shared.models.corps import CorpsModel
from infrastructure.django_apps.shared.models.offer import OfferModel


class OfferAdmin(admin.ModelAdmin):
    """Admin interface for Offer model (read-only)."""

    list_display = (
        "id",
        "external_id",
        "verse",
        "title",
        "category",
        "region",
        "department",
        "limit_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("verse", "category", "region", "created_at", "updated_at")
    search_fields = ("external_id", "title", "profile")
    readonly_fields = (
        "id",
        "external_id",
        "verse",
        "title",
        "profile",
        "category",
        "region",
        "department",
        "limit_date",
        "created_at",
        "updated_at",
    )


class RawDocumentAdmin(admin.ModelAdmin):
    """Admin interface for RawDocument model."""

    list_display = (
        "id",
        "external_id",
        "document_type",
        "raw_data",
        "created_at",
        "updated_at",
    )
    list_filter = ("document_type", "created_at", "updated_at")


class CorpsAdmin(admin.ModelAdmin):
    """Admin interface for Corps model."""

    list_display = (
        "id",
        "code",
        "short_label",
        "long_label",
        "category",
        "ministry",
        "diploma_level",
        "access_modalities",
    )
    list_filter = ("category", "ministry", "diploma_level")
    search_fields = ("code", "short_label", "long_label")
    readonly_fields = ("id", "created_at", "updated_at")

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


class ConcoursAdmin(admin.ModelAdmin):
    """Admin interface for Concours model."""

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
    readonly_fields = ("id", "created_at", "updated_at")

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


class VectorizedDocumentAdmin(admin.ModelAdmin):
    """Admin interface for VectorizedDocument model."""

    list_display = (
        "id",
        "document_id",
        "document_type",
        "content",
        "metadata",
        "created_at",
        "updated_at",
    )
    list_filter = ("document_type", "created_at", "updated_at")
    search_fields = ("document_id", "content")
    readonly_fields = (
        "id",
        "content",
        "metadata",
        "created_at",
        "updated_at",
    )


admin.site.register(RawDocument, RawDocumentAdmin)
admin.site.register(OfferModel, OfferAdmin)
admin.site.register(CorpsModel, CorpsAdmin)
admin.site.register(ConcoursModel, ConcoursAdmin)
admin.site.register(
    vectorized_document.VectorizedDocumentModel, VectorizedDocumentAdmin
)
