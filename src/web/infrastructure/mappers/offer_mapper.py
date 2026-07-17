from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper
from pydantic import HttpUrl
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.offer import OfferModel


class OfferMapper(
    IFromDomainMapper[Offer, OfferModel], IToDomainMapper[OfferModel, Offer]
):
    def to_domain(self, model: OfferModel) -> Offer:
        localisation = None

        if model.region and model.department and model.country and model.area:
            localisation = Localisation(
                area=GeographicalArea(model.area),
                country=Country(model.country),
                region=Region(code=model.region),
                department=Department(code=model.department),
                label=model.location_label,
                latitude=model.latitude,
                longitude=model.longitude,
            )

        beginning_date = (
            LimitDate(model.beginning_date) if model.beginning_date else None
        )
        category = Category(model.category) if model.category else None
        contract_type = (
            ContractType(model.contract_type) if model.contract_type else None
        )
        offer_url = HttpUrl(model.offer_url) if model.offer_url else None
        verse = Verse(model.verse) if model.verse else None

        contract_kind = (
            [ContractKind[name] for name in model.contract_kind]
            if model.contract_kind
            else None
        )

        return Offer(
            id=model.id,
            external_id=model.external_id,
            verse=verse,
            title=model.title,
            profile=model.profile,
            mission=model.mission,
            category=category,
            contract_type=contract_type,
            organization=model.organization,
            offer_url=offer_url,
            localisation=localisation,
            publication_date=model.publication_date,
            beginning_date=beginning_date,
            reference=model.reference,
            processing=model.processing,
            processed_at=model.processed_at,
            archived_at=model.archived_at,
            family_code=model.code_emploi_csp,
            source_id=model.source_id,
            long_title=model.long_title,
            application_url=HttpUrl(model.application_url)
            if model.application_url
            else None,
            contract_kind=contract_kind,
            job_vacancy=model.job_vacancy,
            employer=model.employer,
            complements=model.complements,
            criteria=model.criteria,
            conditions=model.conditions,
            contacts=model.contacts,
        )

    def from_domain(self, entity: Offer) -> OfferModel:
        area = None
        country = None
        region = None
        department = None
        location_label = None
        latitude = None
        longitude = None
        if entity.localisation:
            area = entity.localisation.area.value
            country = str(entity.localisation.country)
            region = entity.localisation.region.code
            department = entity.localisation.department.code
            location_label = entity.localisation.label
            latitude = entity.localisation.latitude
            longitude = entity.localisation.longitude

        beginning_date = entity.beginning_date.value if entity.beginning_date else None
        category = entity.category.value if entity.category else None
        contract_type = entity.contract_type.value if entity.contract_type else None
        offer_url = str(entity.offer_url) if entity.offer_url else None

        contract_kind = (
            [ck.name for ck in entity.contract_kind] if entity.contract_kind else None
        )

        return OfferModel(
            id=entity.id,
            external_id=entity.external_id,
            reference=entity.reference,
            verse=entity.verse.value if entity.verse else None,
            title=entity.title,
            profile=entity.profile,
            mission=entity.mission,
            category=category,
            contract_type=contract_type,
            organization=entity.organization,
            offer_url=offer_url,
            area=area,
            country=country,
            region=region,
            department=department,
            location_label=location_label,
            latitude=latitude,
            longitude=longitude,
            code_emploi_csp=entity.family_code,
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
            contract_kind=contract_kind,
            job_vacancy=entity.job_vacancy,
            employer=entity.employer,
            complements=entity.complements,
            criteria=entity.criteria,
            conditions=entity.conditions,
            contacts=entity.contacts,
        )
