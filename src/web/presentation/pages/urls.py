"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import (
    AccessibilityView,
    ApiChangelogView,
    ApiGuideView,
    HomeView,
    LegalNoticesView,
    OfferDetailView,
    OfferFavoriteView,
    OffersView,
    PrivacyView,
    TermsView,
    TerritoryView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("offres", OffersView.as_view(), name="offers"),
    path("offres/<int:offer_id>", OfferDetailView.as_view(), name="offer_detail"),
    path(
        "offres/<int:offer_id>/favori",
        OfferFavoriteView.as_view(),
        name="offer_favorite",
    ),
    path("territoire/<slug:slug>", TerritoryView.as_view(), name="territory"),
    path("conditions-generales", TermsView.as_view(), name="terms"),
    path("accessibilite", AccessibilityView.as_view(), name="accessibility"),
    path("confidentialite", PrivacyView.as_view(), name="privacy"),
    path("mentions-legales", LegalNoticesView.as_view(), name="legal_notices"),
    path("pages/guide_api", ApiGuideView.as_view(), name="api_guide"),
    path("pages/changelog_api", ApiChangelogView.as_view(), name="api_changelog"),
]
