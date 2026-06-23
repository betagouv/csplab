from django.urls import path

from presentation.recruteur.views import (
    EtapesRecrutementOrganismeView,
    InitEtapesRecrutementOrganismeView,
    OrganismeView,
    RecrutementsOrganismeView,
)

app_name = "recruteur"

urlpatterns = [
    path(
        "organisme/<uuid:organisme_uuid>",
        OrganismeView.as_view(),
        name="organisme",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/parametres/etapes",
        EtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/parametres/etapes/init",
        InitEtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes-init",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements/",
        RecrutementsOrganismeView.as_view(),
        name="organisme-recrutements",
    ),
]
