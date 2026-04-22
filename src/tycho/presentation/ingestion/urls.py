from django.urls import path

from presentation.ingestion.views import ConcoursUploadView

app_name = "ingestion"
urlpatterns = [
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours_upload"),
]
