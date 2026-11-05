from typing import Optional

from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from pydantic import HttpUrl
from referentiel.entities.offer import Offer
from referentiel.entities.talentsoft_organisme import TalentsoftOrganisme
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.offer_criteria import OfferCriteria
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.offer import OfferModel


class OfferMapper(
    IFromDomainMapper[Offer, OfferModel], IToDomainMapper[OfferModel, Offer]
):
    def to_domain(self, model: OfferModel) -> Offer:
        beginning_date = (
            LimitDate(model.beginning_date) if model.beginning_date else None
        )
        offer_nature = OfferNature(model.offer_nature) if model.offer_nature else None
        offer_url = HttpUrl(model.offer_url) if model.offer_url else None
        verse = Verse(model.verse) if model.verse else None

        contract_kind = (
            ContractKind[model.contract_kind] if model.contract_kind else None
        )

        return Offer(
            id=model.id,
            verse=verse,
            title=model.title,
            profile=model.profile,
            mission=model.mission,
            categories=[Category(c) for c in model.categories],
            offer_nature=offer_nature,
            organization=model.organization,
            offer_url=offer_url,
            localisations=[
                localisation.to_localisation()
                for localisation in model.localisations.all()
            ],
            publication_date=model.publication_date,
            beginning_date=beginning_date,
            reference=model.reference,
            processing=model.processing,
            processed_at=model.processed_at,
            archived_at=model.archived_at,
            family_code=model.code_emploi_csp,
            job_family_referential=model.job_family_referential,
            local_job_code=model.local_job_code,
            functional_area_code=model.functional_area_code,
            source_id=model.source_id,
            long_title=model.long_title,
            application_url=HttpUrl(model.application_url)
            if model.application_url
            else None,
            application_email=model.application_email,
            contract_kind=contract_kind,
            job_vacancy=model.job_vacancy,
            employer=model.employer,
            complements=model.complements,
            exercise_conditions=model.exercise_conditions,
            service_description=model.service_description,
            end_publication_date=model.end_publication_date,
            application_deadline=model.application_deadline,
            job_vacancy_date=model.job_vacancy_date,
            criteria=OfferCriteria.from_dict(model.criteria),
            conditions=model.conditions,
            contacts=model.contacts,
            talentsoft_organisme_entity_code=model.talentsoft_organisme_entity_code_id,
            talentsoft_organisme=self._talentsoft_organisme(model),
        )

    @staticmethod
    def _talentsoft_organisme(model: OfferModel) -> Optional[TalentsoftOrganisme]:
        if not OfferModel.talentsoft_organisme_entity_code.is_cached(model):
            return None
        organisme = model.talentsoft_organisme_entity_code
        return organisme.to_entity() if organisme else None

    def from_domain(self, entity: Offer) -> OfferModel:
        beginning_date = entity.beginning_date.value if entity.beginning_date else None
        offer_nature = entity.offer_nature.value if entity.offer_nature else None
        offer_url = str(entity.offer_url) if entity.offer_url else None

        contract_kind = entity.contract_kind.name if entity.contract_kind else None

        return OfferModel(
            id=entity.id,
            reference=entity.reference,
            verse=entity.verse.value if entity.verse else None,
            title=entity.title,
            profile=entity.profile,
            mission=entity.mission,
            categories=[c.value for c in entity.categories],
            offer_nature=offer_nature,
            organization=entity.organization,
            offer_url=offer_url,
            code_emploi_csp=entity.family_code,
            job_family_referential=entity.job_family_referential,
            local_job_code=entity.local_job_code,
            functional_area_code=entity.functional_area_code,
            source_id=entity.source_id,
            publication_date=entity.publication_date,
            beginning_date=beginning_date,
            processing=entity.processing,
            processed_at=entity.processed_at,
            archived_at=entity.archived_at,
            long_title=entity.long_title,
            application_url=str(entity.application_url)
            if entity.application_url
            else None,
            application_email=entity.application_email,
            contract_kind=contract_kind,
            job_vacancy=entity.job_vacancy,
            employer=entity.employer,
            complements=entity.complements,
            exercise_conditions=entity.exercise_conditions,
            service_description=entity.service_description,
            end_publication_date=entity.end_publication_date,
            application_deadline=entity.application_deadline,
            job_vacancy_date=entity.job_vacancy_date,
            criteria=entity.criteria.to_dict() if entity.criteria else None,
            conditions=entity.conditions,
            contacts=entity.contacts,
            talentsoft_organisme_entity_code_id=entity.talentsoft_organisme_entity_code,
        )
