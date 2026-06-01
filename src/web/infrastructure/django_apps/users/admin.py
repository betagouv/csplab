from django.contrib import admin

from infrastructure.django_apps.users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "date_joined",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("email",)
    readonly_fields = [f.name for f in UserModel._meta.get_fields()]
