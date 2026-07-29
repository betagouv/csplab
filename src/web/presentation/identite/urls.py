from django.urls import path

from presentation.identite.views import (
    LoginView,
    ProconnectCallbackView,
    ProconnectLoginView,
    ProconnectLogoutView,
    ProfileView,
    UtilisateurDetailsView,
)

app_name = "identite"

urlpatterns = [
    path("connexion", LoginView.as_view(), name="login"),
    path("deconnexion", ProconnectLogoutView.as_view(), name="logout"),
    path(
        "proconnect/connexion",
        ProconnectLoginView.as_view(),
        name="proconnect_login",
    ),
    path(
        "proconnect/callback",
        ProconnectCallbackView.as_view(),
        name="proconnect_callback",
    ),
    path("profil", ProfileView.as_view(), name="profile"),
    path("me", UtilisateurDetailsView.as_view(), name="user-details"),
]
