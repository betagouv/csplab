from infrastructure.django_apps.users.models import UserModel


def can_view_sources(user: UserModel) -> bool:
    if user.is_superuser:
        return True
    has_agent_profile = hasattr(user, "profil_agent")
    if user.is_staff:
        return has_agent_profile
    return has_agent_profile or user.sources.exists()
