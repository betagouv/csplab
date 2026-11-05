from django.conf import settings
from django.contrib import admin, messages

from application.identite.services.deactivate_api_account import (
    deactivate_api_account,
)
from application.identite.services.revoke_api_tokens import revoke_api_tokens
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
    actions = ("revoke_api_tokens", "deactivate_api_accounts")

    def get_queryset(self, request):
        return super().get_queryset(request).avec_restriction_ip()

    @admin.display(
        boolean=True, description="Restreint par IP", ordering="ip_restricted"
    )
    def is_ip_restricted(self, obj: UserModel) -> bool:
        return obj.ip_restricted  # type: ignore[attr-defined]

    @admin.action(
        description="Révoquer les jetons de rafraîchissement de l'API",
        permissions=["change"],
    )
    def revoke_api_tokens(self, request, queryset):
        revoked = sum(
            revoke_api_tokens(compte=compte, utilisateur=request.user)
            for compte in queryset
        )
        access_minutes = int(
            settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds() // 60
        )
        self.message_user(
            request,
            f"{revoked} jeton(s) de rafraîchissement révoqué(s) pour "
            f"{len(queryset)} compte(s). Les jetons d'accès déjà émis restent "
            f"valables {access_minutes} minutes au plus.",
            messages.SUCCESS,
        )

    @admin.action(
        description="Révoquer les jetons et désactiver le compte",
        permissions=["change"],
    )
    def deactivate_api_accounts(self, request, queryset):
        if queryset.filter(pk=request.user.pk).exists():
            self.message_user(
                request,
                "Vous ne pouvez pas désactiver votre propre compte.",
                messages.ERROR,
            )
            return
        revoked = sum(
            deactivate_api_account(compte=compte, utilisateur=request.user)
            for compte in queryset
        )
        self.message_user(
            request,
            f"{len(queryset)} compte(s) désactivé(s), {revoked} jeton(s) de "
            "rafraîchissement révoqué(s). Plus aucun jeton ne peut être obtenu "
            "ni utilisé pour ces comptes.",
            messages.SUCCESS,
        )


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
