from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.factories.seed_recruteur_datas import seed_recruteur_datas
from infrastructure.factories.seed_recruteur_volume import (
    _VOLUMES_BY_OFFER_REFERENCE,
    seed_recruteur_volume,
)

NB_VOLUME_CANDIDATURES = sum(
    volume
    for volumes in _VOLUMES_BY_OFFER_REFERENCE.values()
    for volume in volumes.values()
)


def _annotate_one_volume_candidature():
    candidature = CandidatureModel.objects.filter(
        candidat__utilisateur__email__endswith="@volume.candidat.fr"
    ).first()
    NoteDjangoFactory(candidature=candidature)
    ConversationDjangoFactory(candidature=candidature)


class TestSeedRecruteurVolume:
    def test_requires_the_base_seed(self, db):
        assert seed_recruteur_volume() == {"status": "base_missing"}

    def test_spreads_candidatures_over_every_etape_and_survives_a_reseed(self, db):
        seed_recruteur_datas()
        nb_base_candidatures = CandidatureModel.objects.count()

        seed_recruteur_volume()
        _annotate_one_volume_candidature()
        seed_recruteur_volume(force=True)

        assert (
            CandidatureModel.objects.count()
            == nb_base_candidatures + NB_VOLUME_CANDIDATURES
        )
        etapes_remplies = (
            CandidatureModel.objects.filter(
                etape__recrutement__offre__reference="REF-2025-001"
            )
            .values("etape")
            .distinct()
        )
        assert etapes_remplies.count() == len(
            _VOLUMES_BY_OFFER_REFERENCE["REF-2025-001"]
        )
        assert not CandidatureModel.objects.filter(
            etape__nom="Refus", motif_refus__isnull=True
        ).exists()

    def test_base_reseed_removes_volume_candidatures(self, db):
        seed_recruteur_datas()
        nb_base_candidatures = CandidatureModel.objects.count()
        seed_recruteur_volume()
        _annotate_one_volume_candidature()

        seed_recruteur_datas(force=True)
        assert CandidatureModel.objects.count() == nb_base_candidatures

        assert seed_recruteur_volume()["status"] == "seeded"

    def test_names_a_renamed_etape(self, db):
        seed_recruteur_datas()
        EtapeModel.objects.filter(
            recrutement__offre__reference="REF-2025-001", nom="Entretien"
        ).update(nom="Entretien RH")

        assert seed_recruteur_volume() == {
            "status": "etape_missing",
            "reference": "REF-2025-001",
            "etape": "Entretien",
        }
