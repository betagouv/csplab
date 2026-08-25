from typing import Optional

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from rest_framework.request import Request

from domain.identite.entities.utilisateurs import Utilisateur
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur


class UtilisateurMapper(
    IToDomainMapper[Request, Utilisateur],
):
    def to_domain(self, model: Request) -> Utilisateur:
        return Utilisateur(
            entity_id=model.username,
            email=model.email,
            prenom=model.first_name,
            nom=model.last_name,
            is_superuser=model.is_superuser,
            is_staff=model.is_staff,
        )


class EtapesMapper(IFromDomainMapper[OrganismeRecruteur, list[dict]]):
    def from_domain(
        self, domain_object: Optional[OrganismeRecruteur]
    ) -> Optional[list[dict]]:
        if domain_object is None:
            return None
        return [
            {
                "etape_uuid": str(e.entity_id),
                "nom": e.nom,
                "categorie": e.categorie.name,
            }
            for e in (domain_object.etapes or ())
        ]
