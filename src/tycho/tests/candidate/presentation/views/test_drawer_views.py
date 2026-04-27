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
    "factory,url_name,id_kwarg,expected_texts",
    [
        (
            _create_offer,
            "candidate:offer_drawer",
            "offer_id",
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
            ["Test Corps Title", "Test Grade Description"],
        ),
    ],
    ids=["offer", "concours"],
)
def test_htmx_request_returns_drawer_partial(
    client, db, factory, url_name, id_kwarg, expected_texts
):
    entity = factory()
    response = client.get(
        reverse(url_name, kwargs={"cv_uuid": uuid4(), id_kwarg: entity.id}),
        headers={"HX-Request": "true"},
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(
        response, "candidate/components/_opportunity_drawer_content.html"
    )
    for text in expected_texts:
        assertContains(response, text)


@pytest.mark.parametrize(
    "factory,url_name,id_kwarg,expected_texts",
    [
        (
            _create_offer,
            "candidate:offer_drawer",
            "offer_id",
            ["Test Offer Title", "Test mission description"],
        ),
        (
            _create_concours,
            "candidate:concours_drawer",
            "concours_id",
            ["Test Corps Title", "Test Grade Description"],
        ),
    ],
    ids=["offer", "concours"],
)
def test_regular_request_returns_full_page(
    client, db, factory, url_name, id_kwarg, expected_texts
):
    entity = factory()
    cv_uuid = uuid4()
    response = client.get(
        reverse(url_name, kwargs={"cv_uuid": cv_uuid, id_kwarg: entity.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/opportunity_detail.html")
    assertTemplateUsed(
        response, "candidate/components/_opportunity_detail_content.html"
    )
    assertContains(
        response, reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid})
    )
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
def test_returns_404_for_unknown_id(client, db, url_name, id_kwarg):
    response = client.get(
        reverse(url_name, kwargs={"cv_uuid": uuid4(), id_kwarg: uuid4()})
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
