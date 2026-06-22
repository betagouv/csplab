"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import (
    AccessibilityView,
    ApiGuideView,
    HomeView,
    LegalNoticesView,
    PrivacyView,
    TermsView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("conditions-generales", TermsView.as_view(), name="terms"),
    path("accessibilite", AccessibilityView.as_view(), name="accessibility"),
    path("confidentialite", PrivacyView.as_view(), name="privacy"),
    path("mentions-legales", LegalNoticesView.as_view(), name="legal_notices"),
    path("pages/guide_api", ApiGuideView.as_view(), name="api_guide"),
]
