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
        # Phase actuelle : données statiques déjà au bon format.
        # Quand le use case sera branché, on mappera ici l'entité → dict.
        return domain_object


class RecrutementListeMapper(IFromDomainMapper[dict, list[dict]]):
    def from_domain(self, domain_object: Optional[dict]) -> Optional[list[dict]]:
        if domain_object is None:
            return None
        result = []
        for etape in domain_object["etapes"]:
            etape_dto = {
                "etape_uuid": etape["etape_uuid"],
                "nom": etape["nom"],
                "categorie": etape["categorie"],
            }
            for candidature in etape["candidatures"]:
                result.append({**candidature, "etape": etape_dto})
        return result
