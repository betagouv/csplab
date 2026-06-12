from dataclasses import dataclass

from pydantic import EmailStr

from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.candidat_errors import ProfilCandidatAlreadyExists
from domain.identite.errors.identite_errors import UtilisateurDoesNotExist
from domain.identite.events.candidat_events import ProfilCandidatCree
from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)
from domain.identite.repositories.utilisateur_repository_interface import (
    IUtilisateurRepository,
)


@dataclass
class CreateCandidatInput:
    email: EmailStr
    prenom: str
    nom: str
    resume: str


class CreateCandidatUsecase:
    def __init__(
        self,
        candidat_repository: ICandidatRepository,
        utilisateur_repository: IUtilisateurRepository,
    ):
        self.candidat_repository = candidat_repository
        self.utilisateur_repository = utilisateur_repository

    def execute(self, input_data: CreateCandidatInput) -> Candidat:
        existing = self.candidat_repository.get_by_email(input_data.email)
        if existing is not None:
            raise ProfilCandidatAlreadyExists(input_data.email)

        event = ProfilCandidatCree(
            email=input_data.email,
            prenom=input_data.prenom,
            nom=input_data.nom,
            resume=input_data.resume,
        )

        try:
            utilisateur = self.utilisateur_repository.get_by_email(input_data.email)
            candidat = Candidat.create(event, entity_id=utilisateur.entity_id)
        except UtilisateurDoesNotExist:
            candidat = Candidat.create(event)
            utilisateur = self.utilisateur_repository.create(
                Utilisateur(
                    entity_id=candidat.entity_id,
                    email=candidat.email,
                    prenom=candidat.prenom,
                    nom=candidat.nom,
                )
            )

        return self.candidat_repository.create(utilisateur, candidat)
