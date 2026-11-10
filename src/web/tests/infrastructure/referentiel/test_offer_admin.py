from django.contrib import admin
from django.test import RequestFactory

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

PARIS = {"area": "EU", "country": "FRA", "region": "11", "department": "75"}
VERSAILLES = {"area": "EU", "country": "FRA", "region": "11", "department": "78"}
CAEN = {"area": "EU", "country": "FRA", "region": "28", "department": "14"}


def test_region_filter_returns_each_offer_once(db):
    paris_and_versailles = OfferDjangoFactory(localisations=[PARIS, VERSAILLES])
    OfferDjangoFactory(localisations=[CAEN])
    request = RequestFactory().get("/", {"localisations__region": "11"})
    request.user = UtilisateurDjangoFactory(is_staff=True, is_superuser=True)

    changelist = admin.site.get_model_admin(OfferModel).get_changelist_instance(request)

    assert list(changelist.get_queryset(request)) == [paris_and_versailles]
