from django.contrib.auth import views as auth_views
from django.urls import path

from presentation.identite.views import (
    LoginView,
    ProfileView,
    UtilisateurDetailsView,
)

app_name = "identite"

urlpatterns = [
    path("connexion/", LoginView.as_view(), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("profil", ProfileView.as_view(), name="profile"),
    path("me/", UtilisateurDetailsView.as_view(), name="user-details"),
]
