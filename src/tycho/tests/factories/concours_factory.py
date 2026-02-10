"""Factory for generating test Concours instances."""

import random
import string
from datetime import datetime
from typing import List, Optional

from faker import Faker
from faker.providers import BaseProvider

from domain.value_objects.category import Category
from domain.value_objects.ministry import Ministry
from infrastructure.django_apps.shared.models.concours import ConcoursModel


class NorProvider(BaseProvider):
    """Nor Provider class."""

    def nor(self):
        """Random nor generator."""
        letters = string.ascii_uppercase
        return (
            "".join(random.choice(letters) for _ in range(4))
            + "".join(random.choice(string.digits) for _ in range(7))
            + random.choice(letters)
        )


fake = Faker()
fake.add_provider(NorProvider)


class ConcoursFactory:
    """Factory for creating Concours test instances."""

    @staticmethod
    def create(
        corps: Optional[str] = None,
        grade: Optional[str] = None,
        nor_original: Optional[str] = None,
        nor_list: Optional[List[str]] = None,
        category: Optional[Category] = None,
        ministry: Optional[str] = None,
        access_modality: Optional[List[str]] = None,
        written_exam_date: Optional[datetime] = None,
        open_position_number: Optional[int] = None,
    ) -> ConcoursModel:
        """Create a ConcoursModel instance."""
        if corps is None:
            corps = "Test Corps"

        if grade is None:
            grade = "Test Grade"

        if nor_original is None:
            nor_original = fake.nor()

        if nor_list is None:
            nor_list = [nor_original]

        if category is None:
            category = random.choice(list(Category)).value

        if ministry is None:
            ministry = random.choice(list(Ministry)).value

        if access_modality is None:
            access_modality = []

        if open_position_number is None:
            open_position_number = 10

        concours = ConcoursModel(
            corps=corps,
            grade=grade,
            nor_original=nor_original,
            nor_list=nor_list,
            category=str(category),
            ministry=ministry,
            access_modality=access_modality,
            written_exam_date=written_exam_date,
            open_position_number=open_position_number,
        )

        concours.save()

        return concours
