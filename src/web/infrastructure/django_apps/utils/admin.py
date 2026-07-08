from django.db import models


class ReadOnlyAdminMixin:
    def get_readonly_fields(self, request, obj=None):
        return [
            f.name for f in self.model._meta.get_fields() if isinstance(f, models.Field)
        ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
