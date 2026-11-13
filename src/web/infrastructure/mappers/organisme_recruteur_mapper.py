from ddd.mapper_interface import IFromDomainMapper

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement


class OrganismeRecruteurMapper(IFromDomainMapper):
    def from_domain(self, etapes: tuple[EtapeRecrutement, ...]) -> list[dict]:
        return [
            {
                "entity_id": str(etape.entity_id),
                "categorie": etape.categorie.value,
                "nom": etape.nom,
            }
            for etape in etapes
        ]
