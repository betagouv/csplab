from uuid import uuid4

from faker import Faker
from pydantic import HttpUrl

from domain.identite.entities.candidat import Candidat
from infrastructure.django_apps.users.models import ProfilCandidatModel
from tests.factories.identite.utilisateur_factory import UtilisateurFactory

fake = Faker()


class CandidatFactory:
    @staticmethod
    def create_entity(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        resume: str | None = None,
    ) -> Candidat:
        return Candidat.build(
            entity_id=uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            resume=resume or fake.text(max_nb_chars=200),
            linkedin=HttpUrl(fake.url(schemes=["https"])),
        )

    @staticmethod
    def create_model(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        resume: str | None = None,
    ) -> ProfilCandidatModel:
        user = UtilisateurFactory.create_model(email=email, prenom=prenom, nom=nom)
        candidat = CandidatFactory.create_entity(
            email=user.email,
            prenom=user.first_name,
            nom=user.last_name,
            resume=resume,
        )
        profil = ProfilCandidatModel(
            utilisateur_id=user.username,
            resume=candidat.resume,
            linkedin=str(candidat.linkedin),
        )
        profil.save()
        return profil
