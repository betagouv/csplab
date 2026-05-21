from django.urls import re_path

from presentation.ats.views import base

urlpatterns = [
    re_path(r"^.*$", base, name="ats_base"),
]
