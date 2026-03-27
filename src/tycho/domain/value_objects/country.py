"""Country value object."""

from pydantic_extra_types.country import CountryAlpha3


class Country(CountryAlpha3):
    def __str__(self):
        return super().__str__()
