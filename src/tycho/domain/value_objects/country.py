"""Country value object."""

from pydantic_extra_types.country import CountryAlpha3


class Country(CountryAlpha3):
    """Country value object using ISO 3166-1 alpha-3 codes."""

    def __str__(self):
        """Return ISO-3 code as string representation."""
        return super().__str__()  # Returns the ISO-3 code (e.g., "FRA")
