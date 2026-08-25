import math

import pytest

from infrastructure.gateways.lambert93 import lambert93_to_wgs84

# Forward Lambert-93 (RGF93/GRS80) projection, used only to build known test
# vectors by round-tripping through `lambert93_to_wgs84`. Mirrors the same
# reference constants (IGN's NTG_71 algorithm) as the inverse implementation.
_GRS80_ECCENTRICITY = 0.08181919112823853
_LAMBERT93_N = 0.7256077650
_LAMBERT93_C = 11754255.426
_LAMBERT93_XS = 700000.0
_LAMBERT93_YS = 12655612.0499
_LAMBERT93_LON0 = math.radians(3.0)


def _wgs84_to_lambert93(latitude: float, longitude: float) -> tuple[float, float]:
    phi = math.radians(latitude)
    lam = math.radians(longitude)
    e = _GRS80_ECCENTRICITY
    lat_iso = math.log(math.tan(math.pi / 4 + phi / 2)) - e / 2 * math.log(
        (1 + e * math.sin(phi)) / (1 - e * math.sin(phi))
    )
    r = _LAMBERT93_C * math.exp(-_LAMBERT93_N * lat_iso)
    gamma = _LAMBERT93_N * (lam - _LAMBERT93_LON0)
    x = _LAMBERT93_XS + r * math.sin(gamma)
    y = _LAMBERT93_YS - r * math.cos(gamma)
    return x, y


@pytest.mark.parametrize(
    "latitude,longitude",
    [
        (48.8566, 2.3522),  # Paris
        (43.2965, 5.3698),  # Marseille
        (45.7640, 4.8357),  # Lyon
        (41.9174, 8.7386),  # Corsica (edge of metropolitan France)
        (16.2650, -61.5510),  # Guadeloupe (overseas, negative longitude)
    ],
)
def test_lambert93_to_wgs84_round_trips(latitude: float, longitude: float):
    x, y = _wgs84_to_lambert93(latitude, longitude)

    result_latitude, result_longitude = lambert93_to_wgs84(x, y)

    assert result_latitude == pytest.approx(latitude, abs=1e-6)
    assert result_longitude == pytest.approx(longitude, abs=1e-6)
