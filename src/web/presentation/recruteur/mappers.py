from typing import Optional

from ddd.mapper_interface import IFromDomainMapper

from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur


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


class RecrutementKanbanMapper(IFromDomainMapper[dict, dict]):
    def from_domain(self, domain_object: Optional[dict]) -> Optional[dict]:
        if domain_object is None:
            return None
        return domain_object
