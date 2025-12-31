"""Django admin configuration for shared models."""

from django.contrib import admin

from apps.shared.infrastructure.adapters.persistence.models.offer import OfferModel


@admin.register(OfferModel)
class OfferAdmin(admin.ModelAdmin):
    """Admin configuration for Offer model."""

    list_display = [
        "external_id",
        "titre",
        "category",
        "verse",
        "region",
        "department",
        "limit_date",
        "created_at",
    ]

    list_filter = [
        "category",
        "verse",
        "region",
        "department",
        "limit_date",
        "created_at",
    ]

    search_fields = [
        "external_id",
        "titre",
        "profile",
    ]

    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Informations générales",
            {"fields": ("id", "external_id", "titre", "profile")},
        ),
        ("Classification", {"fields": ("category", "verse")}),
        ("Localisation", {"fields": ("region", "department")}),
        ("Dates", {"fields": ("limit_date", "created_at", "updated_at")}),
    )

    ordering = ["-created_at"]

    def get_queryset(self, request):
        """Optimize queryset for admin list view."""
        return super().get_queryset(request).select_related()
