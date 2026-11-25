from django.urls import path

from presentation.editorial.views import ServeFileView

app_name = "editorial"

urlpatterns = [path("serve/", ServeFileView.as_view(), name="serve_file")]
