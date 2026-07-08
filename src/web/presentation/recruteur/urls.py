from django.urls import path

from presentation.recruteur.views.organismes import (
    EtapesRecrutementOrganismeView,
    InitEtapesRecrutementOrganismeView,
    OrganismeView,
)
from presentation.recruteur.views.recrutements import (
    RecrutementKanbanView,
    RecrutementListeView,
    RecrutementsActifsView,
    RecrutementsArchivesView,
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
        "organisme/<uuid:organisme_uuid>/recrutements-actifs",
        RecrutementsActifsView.as_view(),
        name="organisme-recrutements-actifs",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements-archives",
        RecrutementsArchivesView.as_view(),
        name="organisme-recrutements-archives",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/kanban",
        RecrutementKanbanView.as_view(),
        name="organisme-recrutement-kanban",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/liste",
        RecrutementListeView.as_view(),
        name="organisme-recrutement-liste",
    ),
]
