import random
import string
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from django.utils import timezone
from faker import Faker
from faker.providers import BaseProvider
from referentiel.entities.concours import Concours
from referentiel.value_objects.access_modality import AccessModality
from referentiel.value_objects.category import Category
from referentiel.value_objects.ministry import Ministry
from referentiel.value_objects.nor import NOR

from infrastructure.django_apps.referentiel.models.concours import ConcoursModel


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
    def _generate_defaults(
        corps: Optional[str],
        grade: Optional[str],
        nor_original: Optional[NOR],
        nor_list: Optional[List[NOR]],
        category: Optional[Category],
        ministry: Optional[Ministry],
        access_modality: Optional[List[AccessModality]],
        open_position_number: Optional[int],
    ) -> tuple[str, str, NOR, List[NOR], Category, Ministry, List[AccessModality], int]:
        if corps is None:
            corps = "Test Corps"
        if grade is None:
            grade = "Test Grade"
        if nor_original is None:
            nor_original = NOR(fake.nor())
        elif isinstance(nor_original, str):
            nor_original = NOR(nor_original)
        if nor_list is None:
            nor_list = [nor_original]
        else:
            nor_list = [NOR(nor) if isinstance(nor, str) else nor for nor in nor_list]
        if category is None:
            category = random.choice(list(Category))
        elif isinstance(category, str):
            category = Category(category)
        if ministry is None:
            ministry = random.choice(list(Ministry))
        elif isinstance(ministry, str):
            ministry = Ministry(ministry)
        if access_modality is None:
            access_modality = []
        if open_position_number is None:
            open_position_number = 10

        return (
            corps,
            grade,
            nor_original,
            nor_list,
            category,
            ministry,
            access_modality,
            open_position_number,
        )

    @staticmethod
    def create_entity(
        corps: Optional[str] = None,
        grade: Optional[str] = None,
        nor_original: Optional[NOR] = None,
        nor_list: Optional[List[NOR]] = None,
        category: Optional[Category] = None,
        ministry: Optional[Ministry] = None,
        access_modality: Optional[List[AccessModality]] = None,
        written_exam_date: Optional[datetime] = None,
        open_position_number: Optional[int] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
    ) -> Concours:
        (
            corps,
            grade,
            nor_original,
            nor_list,
            category,
            ministry,
            access_modality,
            open_position_number,
        ) = ConcoursFactory._generate_defaults(
            corps,
            grade,
            nor_original,
            nor_list,
            category,
            ministry,
            access_modality,
            open_position_number,
        )

        if processed_at:
            processed_at = timezone.make_aware(processed_at)
        if archived_at:
            archived_at = timezone.make_aware(archived_at)

        return Concours(
            id=uuid4(),
            corps=corps,
            grade=grade,
            nor_original=nor_original,
            nor_list=nor_list,
            category=category,
            ministry=ministry,
            access_modality=access_modality,
            written_exam_date=written_exam_date,
            open_position_number=open_position_number,
            processing=processing,
            processed_at=processed_at,
            archived_at=archived_at,
        )

    @staticmethod
    def create_entity_batch(
        size: int,
        **kwargs,
    ) -> List[Concours]:
        return [ConcoursFactory.create_entity(**kwargs) for _ in range(size)]

    @staticmethod
    def create_model(
        corps: Optional[str] = None,
        grade: Optional[str] = None,
        nor_original: Optional[str] = None,
        nor_list: Optional[List[str]] = None,
        category: Optional[str] = None,
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
    def create_model_batch(
        size: int,
        **kwargs,
    ) -> List[ConcoursModel]:
        return [ConcoursFactory.create_model(**kwargs) for _ in range(size)]
