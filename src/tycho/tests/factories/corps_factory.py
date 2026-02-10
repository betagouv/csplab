"""Factory for generating test Corps instances."""

import random
from typing import List, Optional

from faker import Faker

from domain.value_objects.category import Category
from domain.value_objects.ministry import Ministry
from infrastructure.django_apps.shared.models.corps import CorpsModel

fake = Faker()


class CorpsFactory:
    """Factory for creating Corps test instances."""

    @staticmethod
    def create(
        code: Optional[str] = None,
        category: Optional[Category] = None,
        ministry: Optional[str] = None,
        diploma_level: Optional[int] = None,
        short_label: Optional[str] = None,
        long_label: Optional[str] = None,
        access_modalities: Optional[List[str]] = None,
    ) -> CorpsModel:
        """Create a CorpsModel instance."""
        if code is None:
            code = fake.word()

        if category is None:
            category = random.choice(list(Category)).value

        if ministry is None:
            ministry = random.choice(list(Ministry)).value

        if short_label is None:
            short_label = f"Test Corps {code}"

        if long_label is None:
            long_label = f"Corps Long Label {code}"

        if access_modalities is None:
            access_modalities = []

        corps = CorpsModel(
            code=code,
            category=str(category),
            ministry=ministry,
            diploma_level=diploma_level,
            short_label=short_label,
            long_label=long_label,
            access_modalities=access_modalities,
        )

        corps.save()

        return corps
