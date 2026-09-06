from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from infrastructure.django_apps.referentiel.models.metier import MetierModel


class MetierDjangoFactory(DjangoModelFactory):
    class Meta:
        model = MetierModel
        skip_postgeneration_save = True

    id = factory.LazyFunction(uuid4)
    external_id = factory.Sequence(lambda n: f"{n:08d}")
    libelle_long = factory.Faker("job", locale="fr_FR")
    definition_synthetique = factory.Faker("sentence", locale="fr_FR")
    domaine_fonctionnel_code = factory.Faker(
        "random_element", elements=("JUR", "TRA", "MED")
    )
    offer_family_code = factory.Sequence(lambda n: f"FAM{n:05d}")
    versants = factory.LazyFunction(list)
    conditions_particulieres = factory.LazyFunction(list)
    activites = factory.LazyFunction(list)
    processing = False
    processed_at = None
    archived_at = None

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        MetierModel.objects.filter(pk=self.pk).update(
            updated_at=timezone.make_aware(extracted)
        )
        self.refresh_from_db()
