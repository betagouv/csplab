from typing import Optional

from ddd.mapper_interface import IFromDomainMapper

from application.recruteur.dtos.recrutement_read_models import (
    RecrutementActifsReadModel,
    RecrutementArchivesReadModel,
)
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


class RecrutementsActifsMapper(IFromDomainMapper[RecrutementActifsReadModel, dict]):
    def from_domain(
        self, domain_object: Optional[RecrutementActifsReadModel]
    ) -> Optional[dict]:
        if domain_object is None:
            return None
        return {
            "offer_id": domain_object.offer_id,
            "intitule": domain_object.intitule,
            "reference_csp": domain_object.reference_csp,
            "type_contrat": domain_object.type_contrat,
            "date_publication": domain_object.date_publication,
            "responsables": [{"nom": r.nom} for r in domain_object.responsables],
            "derniere_activite": domain_object.derniere_activite,
            "candidatures": {
                "total": domain_object.candidatures.total,
                "a_traiter": domain_object.candidatures.a_traiter,
                "en_cours": domain_object.candidatures.en_cours,
            },
        }


class RecrutementsArchivesMapper(IFromDomainMapper[RecrutementArchivesReadModel, dict]):
    def from_domain(
        self, domain_object: Optional[RecrutementArchivesReadModel]
    ) -> Optional[dict]:
        if domain_object is None:
            return None
        return {
            "offer_id": domain_object.offer_id,
            "intitule": domain_object.intitule,
            "reference_csp": domain_object.reference_csp,
            "type_contrat": domain_object.type_contrat,
            "date_archivage": domain_object.date_archivage,
            "responsables": [{"nom": r.nom} for r in domain_object.responsables],
            "finalise": domain_object.finalise,
            "recrute": domain_object.recrute,
        }
