"""Views for candidate website."""

from apps.candidate.infrastructure.adapters.website.views.cv_flow import (
    CVConfirmationView,
    CVUploadView,
)
from apps.candidate.infrastructure.adapters.website.views.home import HomeView
from apps.candidate.infrastructure.adapters.website.views.resultats import (
    OpportuniteDetailView,
    ResultatsAnalyseView,
)
from apps.candidate.infrastructure.adapters.website.views.search import CorpsSearchView

__all__ = [
    "HomeView",
    "CVUploadView",
    "CVConfirmationView",
    "ResultatsAnalyseView",
    "OpportuniteDetailView",
    "CorpsSearchView",
]
