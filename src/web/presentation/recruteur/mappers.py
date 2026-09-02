from typing import Optional

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from referentiel.entities.organisme import Organisme
from rest_framework.request import Request

from domain.identite.entities.utilisateurs import Utilisateur
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur


class UtilisateurMapper(
    IToDomainMapper[Request, Utilisateur],
):
    def to_domain(self, request: Request) -> Utilisateur:
        user = request.user
        return Utilisateur(
            entity_id=user.username,
            email=user.email,
            prenom=user.first_name,
            nom=user.last_name,
            is_superuser=user.is_superuser,
            is_staff=user.is_staff,
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


class OrganismeMapper(IFromDomainMapper[Organisme, dict]):
    def from_domain(self, organisme: Organisme) -> dict:
        return {
            "organisme_uuid": str(organisme.entity_id),
            "nom": organisme.nom,
            "siret": str(organisme.siret),
            "versant": organisme.versant.value,
            "gestion_ats": organisme.gestion_ats,
            "date_creation": organisme.date_creation,
            "date_derniere_activite": organisme.date_derniere_activite,
        }
