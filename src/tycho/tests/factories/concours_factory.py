import random
import string
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from django.utils import timezone
from faker import Faker
from faker.providers import BaseProvider

from domain.value_objects.category import Category
from domain.value_objects.ministry import Ministry
from infrastructure.django_apps.shared.models.concours import ConcoursModel


class NorProvider(BaseProvider):
    def nor(self):
        letters = string.ascii_uppercase
        return (
            "".join(random.choice(letters) for _ in range(4))
            + "".join(random.choice(string.digits) for _ in range(7))
            + random.choice(letters)
        )


fake = Faker()
fake.add_provider(NorProvider)


class ConcoursFactory:
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
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
    ) -> ConcoursModel:
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

        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        if archived_at:
            archived_at = timezone.make_aware(archived_at)

        concours = ConcoursModel(
            id=uuid4(),
            corps=corps,
            grade=grade,
            nor_original=nor_original,
            nor_list=nor_list,
            category=str(category),
            ministry=ministry,
            access_modality=access_modality,
            written_exam_date=written_exam_date,
            open_position_number=open_position_number,
            processing=processing,
            processed_at=processed_at,
            archived_at=archived_at,
        )

        concours.save()

        if updated_at:
            ConcoursModel.objects.filter(id=concours.id).update(
                updated_at=timezone.make_aware(updated_at)
            )
            concours.refresh_from_db()

        return concours

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[ConcoursModel]:
        return [ConcoursFactory.create(**kwargs) for _ in range(size)]
