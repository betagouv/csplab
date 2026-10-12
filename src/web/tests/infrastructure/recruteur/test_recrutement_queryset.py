from django.utils import timezone

from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)


def test_active_by_id_excludes_recrutement_of_supprime_organisme(db):
    actif = RecrutementDjangoFactory()
    supprime = RecrutementDjangoFactory(organisme__supprime_le=timezone.now())

    assert list(RecrutementModel.objects.active_by_id(actif.pk)) == [actif]
    assert not RecrutementModel.objects.active_by_id(supprime.pk).exists()
