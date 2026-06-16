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
        "etapes-recrutement-organisme/<uuid:organisme_uuid>/",
        EtapesRecrutementOrganismeView.as_view(),
        name="etapes-recrutement-organisme",
    ),
]
