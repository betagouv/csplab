from django.urls import path

from presentation.ingestion.health import HueyHealthView
from presentation.ingestion.views import ConcoursUploadView

urlpatterns = [
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours-upload"),
    path("health/huey/", HueyHealthView.as_view(), name="health-huey"),
]
