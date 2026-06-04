import pytest
from referentiel.repositories.metier_repository_interface import IMetierRepository

from tests.factories.metier_factory import MetierFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock


@pytest.fixture
def sample_metiers():
    return [
        MetierFactory.create_entity(offer_family_code="ERJUR011"),
        MetierFactory.create_entity(offer_family_code="ERJUR022"),
        MetierFactory.create_entity(offer_family_code="ERTRA033"),
    ]


@pytest.fixture
def metier_repository_mock():
    return create_interface_aware_mock(IMetierRepository)


def test_upsert_batch_stores_entities(metier_repository_mock, sample_metiers):
    metier_repository_mock.upsert_batch(sample_metiers)

    all_metiers = metier_repository_mock.get_all()
    assert len(all_metiers) == len(sample_metiers)

    stored_codes = {m.offer_family_code for m in all_metiers}
    expected_codes = {"ERJUR011", "ERJUR022", "ERTRA033"}
    assert stored_codes == expected_codes


def test_get_filtered_with_matching_offer_family_code(
    metier_repository_mock, sample_metiers
):
    metier_repository_mock.upsert_batch(sample_metiers)

    filtered_metiers = metier_repository_mock.get_filtered(
        {"offer_family_code": "ERJUR011"}
    )

    assert len(filtered_metiers) == 1
    assert filtered_metiers[0].offer_family_code == "ERJUR011"


def test_get_filtered_with_non_matching_offer_family_code(
    metier_repository_mock, sample_metiers
):
    metier_repository_mock.upsert_batch(sample_metiers)

    filtered_metiers = metier_repository_mock.get_filtered(
        {"offer_family_code": "NONEXISTENT"}
    )

    assert len(filtered_metiers) == 0
    assert filtered_metiers == []


def test_get_all_returns_all_stored_entities(metier_repository_mock, sample_metiers):
    metier_repository_mock.upsert_batch(sample_metiers)

    all_metiers = metier_repository_mock.get_all()

    assert len(all_metiers) == len(sample_metiers)
    stored_codes = {m.offer_family_code for m in all_metiers}
    expected_codes = {"ERJUR011", "ERJUR022", "ERTRA033"}
    assert stored_codes == expected_codes
