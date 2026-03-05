"""Integration tests for opportunity drawer views."""

from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from tests.factories.concours_factory import ConcoursFactory
from tests.factories.offer_factory import OfferFactory


def _create_offer():
    return OfferFactory.create(
        title="Test Offer Title",
        profile="Test profile description",
        mission="Test mission description",
    )


def _create_concours():
    return ConcoursFactory.create(
        corps="Test Corps Title", grade="Test Grade Description"
    )


@pytest.mark.parametrize(
    "factory,url_name,id_kwarg,template,expected_texts",
    [
        (
            _create_offer,
            "candidate:offer_drawer",
            "offer_id",
            "candidate/components/_opportunity_drawer_content.html",
            [
                "Test Offer Title",
                "Test profile description",
                "Test mission description",
            ],
        ),
        (
            _create_concours,
            "candidate:concours_drawer",
            "concours_id",
            "candidate/components/_opportunity_drawer_content.html",
            ["Test Corps Title", "Test Grade Description"],
        ),
    ],
    ids=["offer", "concours"],
)
def test_drawer_returns_partial_with_details(
    client, db, factory, url_name, id_kwarg, template, expected_texts
):
    entity = factory()
    response = client.get(
        reverse(url_name, kwargs={"cv_uuid": uuid4(), id_kwarg: entity.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)
    for text in expected_texts:
        assertContains(response, text)


@pytest.mark.parametrize(
    "url_name,id_kwarg",
    [
        ("candidate:offer_drawer", "offer_id"),
        ("candidate:concours_drawer", "concours_id"),
    ],
    ids=["offer", "concours"],
)
def test_drawer_returns_404_for_unknown_id(client, db, url_name, id_kwarg):
    response = client.get(
        reverse(url_name, kwargs={"cv_uuid": uuid4(), id_kwarg: uuid4()})
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
