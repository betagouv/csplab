import pytest
from django.db import IntegrityError, transaction

from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

CONSTRAINT = "offer_categories_not_empty"


def test_offer_without_category_is_rejected(db):
    with pytest.raises(IntegrityError, match=CONSTRAINT), transaction.atomic():
        OfferDjangoFactory(categories=[])
