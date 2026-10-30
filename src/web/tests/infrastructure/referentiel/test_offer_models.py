import pytest
from django.db import IntegrityError, transaction
from referentiel.value_objects.category import Category

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

CONSTRAINT = "offer_categories_not_empty"


def test_offer_without_category_is_rejected(db):
    with pytest.raises(IntegrityError, match=CONSTRAINT), transaction.atomic():
        OfferDjangoFactory(categories=[])


def test_update_removing_all_categories_is_rejected(db):
    offer = OfferDjangoFactory(categories=[Category.A])

    with pytest.raises(IntegrityError, match=CONSTRAINT), transaction.atomic():
        OfferModel.objects.filter(pk=offer.pk).update(categories=[])


def test_bulk_create_without_category_is_rejected(db):
    offer = OfferDjangoFactory.build(categories=[])

    with pytest.raises(IntegrityError, match=CONSTRAINT), transaction.atomic():
        OfferModel.objects.bulk_create([offer])
