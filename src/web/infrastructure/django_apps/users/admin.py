from django.contrib import admin
from django.db.models import Exists, OuterRef

from infrastructure.django_apps.users.models import (
    AllowedNetworkModel,
    ProfilAgentModel,
    ProfilCandidatModel,
    UserModel,
)
from infrastructure.django_apps.utils.admin import ReadOnlyAdminMixin


class AllowedNetworkInline(admin.TabularInline):
    model = AllowedNetworkModel
    fields = ("cidr", "label", "created_at")
    readonly_fields = ("created_at",)
    extra = 0
    template = "admin/users/allowed_network_inline.html"


class IpRestrictedFilter(admin.SimpleListFilter):
    title = "Restreint par IP"
    parameter_name = "ip_restricted"

    def lookups(self, request, model_admin):
        return (("1", "Oui"), ("0", "Non"))

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(ip_restricted=True)
        if self.value() == "0":
            return queryset.filter(ip_restricted=False)
        return queryset


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "date_joined",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_ip_restricted",
    )
    list_filter = ("is_staff", "is_superuser", IpRestrictedFilter)
    search_fields = ("email",)
    readonly_fields = ["username", "id", "date_joined", "last_login", "password"]
    filter_horizontal = ("sources",)
    inlines = (AllowedNetworkInline,)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                ip_restricted=Exists(
                    AllowedNetworkModel.objects.filter(user=OuterRef("pk"))
                )
            )
        )

    @admin.display(
        boolean=True, description="Restreint par IP", ordering="ip_restricted"
    )
    def is_ip_restricted(self, obj: UserModel) -> bool:
        return obj.ip_restricted  # type: ignore[attr-defined]


@admin.register(ProfilCandidatModel)
class ProfilCandidatAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("utilisateur", "created_at", "updated_at")
    search_fields = ("utilisateur__email",)
    date_hierarchy = "created_at"


@admin.register(ProfilAgentModel)
class ProfilAgentAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("utilisateur", "intitule_poste", "created_at", "updated_at")
    search_fields = ("utilisateur__email", "intitule_poste")
    date_hierarchy = "created_at"
