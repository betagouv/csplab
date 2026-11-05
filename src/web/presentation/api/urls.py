from django.urls import path

from presentation.api.token_views import LoggedTokenObtainPairView, TokenRefreshView
from presentation.api.views import (
    ChangelogAtomView,
    ChangelogJsonView,
    ChangelogMarkdownView,
    GuideMarkdownView,
    HueyHealthView,
    PublicSchemaView,
    RedocView,
)

app_name = "api"

urlpatterns = [
    path("token", LoggedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("health/huey", HueyHealthView.as_view(), name="health_huey"),
    path("schema/redoc", RedocView.as_view(), name="redoc"),
    path("schema/public", PublicSchemaView.as_view(), name="public_schema"),
    path("changelog.md", ChangelogMarkdownView.as_view(), name="changelog_markdown"),
    path("changelog.json", ChangelogJsonView.as_view(), name="changelog_json"),
    path("changelog.atom", ChangelogAtomView.as_view(), name="changelog_atom"),
    path("guide.md", GuideMarkdownView.as_view(), name="guide_markdown"),
]
