from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.candidat import Candidat
from infrastructure.django_apps.users.models import ProfilCandidatModel
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory

fake = Faker()


class CandidatFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        resume: str | None = None,
    ) -> Candidat:
        return Candidat.build(
            entity_id=entity_id or uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            resume=resume or fake.text(max_nb_chars=200),
        )

    @staticmethod
    def create_model(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        resume: str | None = None,
    ) -> ProfilCandidatModel:
        candidat = CandidatFactory.create_entity(
            email=email,
            prenom=prenom,
            nom=nom,
            resume=resume,
        )
        user = UtilisateurFactory.create_model(
            entity_id=candidat.entity_id,
            email=candidat.email,
            prenom=candidat.prenom,
            nom=candidat.nom,
        )
        profil = ProfilCandidatModel.from_entity(user.to_entity(), candidat)
        profil.save()
        return profil
