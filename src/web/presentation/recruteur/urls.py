from django.urls import path

from presentation.recruteur.views import EtapesRecrutementOrganismeView, OrganismeView

app_name = "recruteur"

urlpatterns = [
    path(
        "organisme/<uuid:organisme_uuid>/",
        OrganismeView.as_view(),
        name="organisme",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/parametres/etapes/",
        EtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes",
    ),
]
