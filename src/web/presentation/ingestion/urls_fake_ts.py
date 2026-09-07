from django.urls import path

from presentation.ingestion.views.offer_detail import OfferDetailView
from presentation.ingestion.views.offer_summaries import OfferSummariesView
from presentation.ingestion.views.referentials import ReferentialListView

app_name = "ingestion_fake_ts"

urlpatterns = [
    path("offersummaries", OfferSummariesView.as_view(), name="offer_summaries"),
    path("offers/getoffer", OfferDetailView.as_view(), name="offer_detail"),
    path(
        "referentials/<str:type>",
        ReferentialListView.as_view(),
        name="referentials_list",
    ),
]
