from django.urls import re_path

from presentation.ats.views import base

app_name = "ats"

urlpatterns = [
    re_path(r"^.*$", base, name="ats_base"),
]
