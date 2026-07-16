from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from referentiel.entities.metier import Metier
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.metier import MetierModel


class MetierMapper(
    IFromDomainMapper[Metier, MetierModel], IToDomainMapper[MetierModel, Metier]
):
    def to_domain(self, model: MetierModel) -> Metier:
        versants = (
            [Verse(verse) for verse in model.versants if verse]
            if model.versants
            else []
        )

        return Metier(
            id=model.id,
            external_id=model.external_id,
            libelle=model.libelle_long,
            description=model.definition_synthetique or "",
            domaine_fonctionnel_code=model.domaine_fonctionnel_code,
            versants=versants,
            activites=model.activites or [],
            conditions_particulieres=model.conditions_particulieres or [],
            offer_family_code=model.offer_family_code,
        )

    def from_domain(self, entity: Metier) -> MetierModel:
        versants = (
            [verse.value for verse in entity.versants] if entity.versants else None
        )

        return MetierModel(
            id=entity.id,
            external_id=entity.external_id,
            libelle_long=entity.libelle,
            definition_synthetique=entity.description,
            domaine_fonctionnel_code=entity.domaine_fonctionnel_code,
            offer_family_code=entity.offer_family_code or "",
            versants=versants,
            activites=entity.activites,
            conditions_particulieres=entity.conditions_particulieres,
        )
