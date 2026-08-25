import math

# RGF93 / Lambert-93 (EPSG:2154) projection constants, using the GRS80 ellipsoid.
# See IGN's "Algorithmes de transformation de coordonnées" (NTG_71) for the
# reference formulas this inverse projection implements.
_GRS80_ECCENTRICITY = 0.08181919112823853
_LAMBERT93_N = 0.7256077650
_LAMBERT93_C = 11754255.426
_LAMBERT93_XS = 700000.0
_LAMBERT93_YS = 12655612.0499
_LAMBERT93_LON0 = math.radians(3.0)
_CONVERGENCE_ITERATIONS = 6


def lambert93_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """Converts Lambert-93 (EPSG:2154) coordinates, in meters, to WGS84
    (EPSG:4326) (latitude, longitude), in decimal degrees."""
    dx = x - _LAMBERT93_XS
    dy = y - _LAMBERT93_YS
    r = math.hypot(dx, dy)
    gamma = math.atan2(dx, -dy)
    longitude = _LAMBERT93_LON0 + gamma / _LAMBERT93_N
    lat_iso = -math.log(abs(r / _LAMBERT93_C)) / _LAMBERT93_N

    latitude = 2 * math.atan(math.exp(lat_iso)) - math.pi / 2
    for _ in range(_CONVERGENCE_ITERATIONS):
        sin_latitude = math.sin(latitude)
        latitude = (
            2
            * math.atan(
                (
                    (1 + _GRS80_ECCENTRICITY * sin_latitude)
                    / (1 - _GRS80_ECCENTRICITY * sin_latitude)
                )
                ** (_GRS80_ECCENTRICITY / 2)
                * math.exp(lat_iso)
            )
            - math.pi / 2
        )

    return math.degrees(latitude), math.degrees(longitude)
