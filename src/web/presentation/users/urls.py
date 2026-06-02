from django.contrib.auth import views as auth_views
from django.urls import path

from presentation.users.views import ProfileView

app_name = "users"

urlpatterns = [
    path("connexion/", auth_views.LoginView.as_view(), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("profil", ProfileView.as_view(), name="profile"),
]
