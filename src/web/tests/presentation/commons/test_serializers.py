import pytest

from presentation.commons.serializers import LocalisationSerializer


def _payload(**overrides):
    payload = {
        "zone_geographique": "EU",
        "pays": "FRA",
        "region": "",
        "departement": "",
        "localisation_label": "",
        "latitude": None,
        "longitude": None,
    }
    payload.update(overrides)
    return payload


def test_localisation_serializer_accepts_valid_payload():
    serializer = LocalisationSerializer(data=_payload())

    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize("pays", ["FRA", "USA", "DEU"])
def test_localisation_serializer_accepts_valid_alpha3_country_codes(pays):
    serializer = LocalisationSerializer(data=_payload(pays=pays))

    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize("pays", ["XXX", "ZZZ", "AAA"])
def test_localisation_serializer_rejects_invalid_alpha3_country_codes(pays):
    serializer = LocalisationSerializer(data=_payload(pays=pays))

    assert not serializer.is_valid()
    assert "pays" in serializer.errors


def test_localisation_serializer_rejects_country_codes_of_wrong_length():
    serializer = LocalisationSerializer(data=_payload(pays="FR"))

    assert not serializer.is_valid()
    assert "pays" in serializer.errors


@pytest.mark.parametrize("latitude", [-90, 0, 90])
def test_localisation_serializer_accepts_latitude_within_bounds(latitude):
    serializer = LocalisationSerializer(data=_payload(latitude=latitude))

    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize("latitude", [-90.1, 90.1, -180, 180])
def test_localisation_serializer_rejects_latitude_out_of_bounds(latitude):
    serializer = LocalisationSerializer(data=_payload(latitude=latitude))

    assert not serializer.is_valid()
    assert "latitude" in serializer.errors


@pytest.mark.parametrize("longitude", [-180, 0, 180])
def test_localisation_serializer_accepts_longitude_within_bounds(longitude):
    serializer = LocalisationSerializer(data=_payload(longitude=longitude))

    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize("longitude", [-180.1, 180.1])
def test_localisation_serializer_rejects_longitude_out_of_bounds(longitude):
    serializer = LocalisationSerializer(data=_payload(longitude=longitude))

    assert not serializer.is_valid()
    assert "longitude" in serializer.errors


def test_localisation_serializer_allows_null_coordinates():
    serializer = LocalisationSerializer(data=_payload(latitude=None, longitude=None))

    assert serializer.is_valid(), serializer.errors
