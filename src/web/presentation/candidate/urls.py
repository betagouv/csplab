from django.urls import path

from presentation.candidate.views.cv_flow import (
    ConcoursDrawerView,
    CVResultsView,
    CVUploadView,
    OfferDrawerView,
)
from presentation.candidate.views.home import (
    CandidateAlertEditView,
    CandidateAlertView,
    CandidateApplicationDetailView,
    CandidateApplicationsView,
    CandidateConversationsView,
    CandidateDocumentView,
    CandidateFranceConnectView,
    CandidateHomeView,
    CandidateLoginView,
    CandidateLogoutView,
    CandidateOfferView,
    CandidateSavedOfferView,
)

app_name = "candidate"

urlpatterns = [
    path("", CandidateHomeView.as_view(), name="home"),
    path(
        "mes-candidatures",
        CandidateApplicationsView.as_view(),
        name="applications",
    ),
    path(
        "mes-candidatures/<int:application_id>",
        CandidateApplicationDetailView.as_view(),
        name="application_detail",
    ),
    path(
        "mes-candidatures/<int:application_id>/conversations",
        CandidateConversationsView.as_view(),
        name="conversations",
    ),
    path(
        "mes-candidatures/<int:application_id>/conversations/<int:conversation_id>",
        CandidateConversationsView.as_view(),
        name="conversation",
    ),
    path(
        "mes-candidatures/<int:application_id>/documents/<slug:slug>",
        CandidateDocumentView.as_view(),
        name="document",
    ),
    path(
        "mes-candidatures/<int:application_id>/offre",
        CandidateOfferView.as_view(),
        name="offer",
    ),
    path(
        "mon-alerte/modifier",
        CandidateAlertEditView.as_view(),
        name="alert_edit",
    ),
    path("mon-alerte", CandidateAlertView.as_view(), name="alert"),
    path(
        "mes-offres/<int:offer_id>",
        CandidateSavedOfferView.as_view(),
        name="saved_offer",
    ),
    path(
        "connexion/franceconnect",
        CandidateFranceConnectView.as_view(),
        name="franceconnect",
    ),
    path("deconnexion", CandidateLogoutView.as_view(), name="logout"),
    path("connexion", CandidateLoginView.as_view(), name="login"),
    path("cv-upload", CVUploadView.as_view(), name="cv_upload"),
    path(
        "cv/<uuid:cv_uuid>/results",
        CVResultsView.as_view(),
        name="cv_results",
    ),
    path(
        "cv/<uuid:cv_uuid>/offers/<uuid:offer_id>/detail",
        OfferDrawerView.as_view(),
        name="offer_drawer",
    ),
    path(
        "cv/<uuid:cv_uuid>/concours/<uuid:concours_id>/detail",
        ConcoursDrawerView.as_view(),
        name="concours_drawer",
    ),
]
