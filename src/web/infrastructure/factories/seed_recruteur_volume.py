from datetime import timedelta
from itertools import cycle

from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementModel,
)
from infrastructure.django_apps.users.models import ProfilCandidatModel, UserModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.seed_recruteur_datas import (
    _seed_cv,
    delete_candidatures,
)

_VOLUME_EMAIL_DOMAIN = "@volume.candidat.fr"
_CV_EVERY = 10
_CREATED_WITHIN = timedelta(days=60)

# 105 exceeds one API page (100); 13 spans three list pages of 6.
_VOLUMES_BY_OFFER_REFERENCE = {
    "REF-2025-001": {
        "Réception des candidatures": 120,
        "Présélection": 60,
        "Entretien": 40,
        "Proposition": 15,
        "Refus": 50,
        "Recrutement": 15,
    },
    "REF-2025-002": {"Réception des candidatures": 105},
    "REF-2025-003": {"Réception des candidatures": 13},
}


def _delete_volume_data() -> None:
    delete_candidatures(
        list(
            CandidatureModel.objects.filter(
                candidat__utilisateur__email__endswith=_VOLUME_EMAIL_DOMAIN
            ).values_list("id", flat=True)
        )
    )
    ProfilCandidatModel.objects.filter(
        utilisateur__email__endswith=_VOLUME_EMAIL_DOMAIN
    ).delete()
    UserModel.objects.filter(email__endswith=_VOLUME_EMAIL_DOMAIN).delete()


def seed_recruteur_volume(force: bool = False) -> dict:
    recrutements = RecrutementModel.objects.filter(
        offre__reference__in=_VOLUMES_BY_OFFER_REFERENCE
    ).select_related("offre")
    if recrutements.count() < len(_VOLUMES_BY_OFFER_REFERENCE):
        return {"status": "base_missing"}
    etapes_by_reference = {
        r.offre.reference: {e.nom: e for e in r.etapes.all()}  # type: ignore[attr-defined]
        for r in recrutements
    }
    for reference, volumes in _VOLUMES_BY_OFFER_REFERENCE.items():
        for nom_etape in volumes:
            if nom_etape not in etapes_by_reference[reference]:
                return {
                    "status": "etape_missing",
                    "reference": reference,
                    "etape": nom_etape,
                }
    if (
        CandidatureModel.objects.filter(
            candidat__utilisateur__email__endswith=_VOLUME_EMAIL_DOMAIN
        ).exists()
        and not force
    ):
        return {"status": "already_seeded"}

    fake = Faker("fr_FR")
    fake.seed_instance(0)
    motifs_refus = cycle(MotifRefus.values)
    now = timezone.now()
    candidatures: list[CandidatureModel] = []

    with transaction.atomic():
        _delete_volume_data()
        for reference, volumes in _VOLUMES_BY_OFFER_REFERENCE.items():
            for nom_etape, volume in volumes.items():
                etape = etapes_by_reference[reference][nom_etape]
                refus = etape.categorie == CategorieEtapeRecrutement.REFUS.value
                for _ in range(volume):
                    prenom, nom = fake.first_name(), fake.last_name()
                    candidat = CandidatDjangoFactory(
                        utilisateur__first_name=prenom,
                        utilisateur__last_name=nom,
                        utilisateur__email=(
                            f"{slugify(prenom)}.{slugify(nom)}"
                            f".{len(candidatures)}{_VOLUME_EMAIL_DOMAIN}"
                        ),
                        utilisateur__password=None,
                    )
                    candidature: CandidatureModel = CandidatureDjangoFactory(  # type: ignore[assignment]
                        candidat=candidat,
                        etape=etape,
                        statut=StatutCandidature.SOUMISE.value,
                        motif_refus=next(motifs_refus) if refus else None,
                    )
                    if len(candidatures) % _CV_EVERY == 0:
                        _seed_cv(candidature, candidat.utilisateur)  # type: ignore[arg-type]
                    candidature.created_at = fake.date_time_between(
                        now - _CREATED_WITHIN, now, tzinfo=now.tzinfo
                    )
                    candidatures.append(candidature)
        CandidatureModel.objects.bulk_update(candidatures, ["created_at"])

    return {"status": "seeded", "nb_candidatures": len(candidatures)}
