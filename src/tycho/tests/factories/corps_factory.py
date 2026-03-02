import random
from datetime import datetime
from typing import List, Optional

from django.utils import timezone
from faker import Faker

from domain.entities.corps import Corps
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.label import Label
from domain.value_objects.ministry import Ministry
from infrastructure.django_apps.shared.models.corps import CorpsModel

fake = Faker()


class CorpsFactory:
    @staticmethod
    def create(
        code: Optional[str] = None,
        category: Optional[Category] = None,
        ministry: Optional[str] = None,
        diploma_level: Optional[int] = None,
        short_label: Optional[str] = None,
        long_label: Optional[str] = None,
        access_modalities: Optional[List[str]] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
    ) -> CorpsModel:
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

        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        if archived_at:
            archived_at = timezone.make_aware(archived_at)

        entity = Corps(
            code=code,
            category=Category(category) if isinstance(category, str) else category,
            ministry=Ministry(ministry) if isinstance(ministry, str) else ministry,
            diploma=None,  # Will be set if diploma_level provided
            access_modalities=[AccessModality(mod) for mod in access_modalities]
            if access_modalities
            else [],
            label=Label(short_value=short_label, value=long_label),
            processing=processing,
            processed_at=processed_at,
            archived_at=archived_at,
        )

        corps = CorpsModel.from_entity(entity)
        corps.save()

        if updated_at:
            CorpsModel.objects.filter(id=corps.id).update(
                updated_at=timezone.make_aware(updated_at)
            )
            corps.refresh_from_db()

        return corps

    @staticmethod
    def create_batch(
        size: int,
        **kwargs,
    ) -> List[CorpsModel]:
        return [CorpsFactory.create(**kwargs) for _ in range(size)]
