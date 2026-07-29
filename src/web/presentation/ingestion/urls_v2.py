from django.urls import path

from presentation.ingestion.views.offer_summaries import OfferSummariesView

app_name = "ingestion_v2"

urlpatterns = [
    path("offersummaries", OfferSummariesView.as_view(), name="offer_summaries"),
]
