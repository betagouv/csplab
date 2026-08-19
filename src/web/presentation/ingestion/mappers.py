from datetime import datetime
from typing import Optional
from uuid import UUID

from ddd.mapper_interface import IToDomainMapper
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_criteria import OfferCriteria, OfferLanguage
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse


class LocalisationInputMapper(IToDomainMapper[dict, Localisation]):
    def to_domain(self, data: Optional[dict]) -> Optional[Localisation]:
        if not data:
            return None
        return Localisation(
            area=GeographicalArea(data["zone_geographique"]),
            country=Country(data["pays"]),
            region=Region(code=data["region"]),
            department=Department(code=data["departement"]),
            label=data.get("localisation_label") or None,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )


class OfferInputMapper(IToDomainMapper[dict, Offer]):
    def __init__(self) -> None:
        self._localisation_mapper = LocalisationInputMapper()

    def to_domain(self, data: Optional[dict], source_id: UUID) -> Optional[Offer]:
        if not data:
            return None

        # todo handle multiple categories offers later
        category = (
            Category(sorted(data["categories"])[0]) if data.get("categories") else None
        )
        conditions = data.get("conditions") or None
        debut_contrat = conditions.get("debut_contrat") if conditions else None

        localisations = data.get("localisation", [])
        raw_localisation = localisations[0] if localisations else None

        forme_contrat = data.get("forme_contrat")

        return Offer(
            external_id=f"{data['identification']['versant']}-{data['identification']['reference']}",
            reference=data["identification"]["reference"],
            title=data["titre"],
            profile=data["description"]["profil"],
            mission=data["description"]["mission"],
            organization=data["organisation"]["nom"],
            publication_date=data["publication"]["debut_publication"],
            verse=Verse(data["identification"]["versant"]),
            category=category,
            contract_type=ContractType(data["type_contrat"]),
            offer_url=data.get("url_offre"),
            localisation=self._localisation_mapper.to_domain(raw_localisation),
            beginning_date=LimitDate(debut_contrat) if debut_contrat else None,
            family_code=data["profession"]["metier"],
            job_family_referential=data["profession"].get("referentiel"),
            local_job_code=data["profession"].get("code_emploi_local"),
            functional_area_code=data["profession"].get("domaine"),
            source_id=source_id,
            long_title=data.get("titre_long") or None,
            application_url=data.get("url_candidature"),
            contract_kind=[ContractKind[name] for name in sorted(forme_contrat)]
            if forme_contrat
            else None,
            job_vacancy=data.get("vacance_poste") or None,
            employer=data["description"].get("employeur") or None,
            complements=data["description"].get("complements") or None,
            criteria=OfferCriteria.from_dict(data.get("criteres")),
            conditions=conditions,
            contacts=list(data["contacts"]) if data.get("contacts") else None,
        )


class OfferSummaryOutputMapper:
    def to_dict(self, offer: Offer) -> dict:
        return {
            "reference": offer.reference,
            "isTopOffer": False,
            "title": offer.title,
            "location": offer.localisation.label if offer.localisation else None,
            "modificationDate": self._isoformat(
                offer.processed_at or offer.publication_date
            ),
            "contractType": self._coded_object(
                offer.contract_type.name, offer.contract_type.value, "contractType"
            )
            if offer.contract_type
            else None,
            "offerFamilyCategory": self._coded_object(
                offer.category.name, offer.category.value, "offerFamilyCategory"
            )
            if offer.category
            else None,
            "organisationName": offer.organization,
            "organisationDescription": offer.employer,
            "organisationLogoUrl": None,
            "contractDuration": None,
            "contractTypeCountry": None,
            "description1": offer.mission,
            "description2": offer.profile,
            "description1Formatted": None,
            "description2Formatted": None,
            "salaryRange": None,
            "geographicalLocation": [],
            "country": [
                self._coded_object(
                    str(offer.localisation.country),
                    offer.localisation.country.short_name,
                    "country",
                )
            ]
            if offer.localisation
            else [],
            "region": [
                self._coded_object(
                    offer.localisation.region.code,
                    offer.localisation.region.name,
                    "region",
                )
            ]
            if offer.localisation
            else [],
            "department": [
                self._coded_object(
                    offer.localisation.department.code,
                    offer.localisation.department.name,
                    "department",
                )
            ]
            if offer.localisation
            else [],
            "latitude": offer.localisation.latitude if offer.localisation else None,
            "longitude": offer.localisation.longitude if offer.localisation else None,
            "professionalCategory": None,
            "_links": [],
            "offerUrl": str(offer.offer_url) if offer.offer_url else None,
            "_format": None,
            "_metadata": None,
            "urlRedirectionEmployee": None,
            "urlRedirectionApplicant": str(offer.application_url)
            if offer.application_url
            else None,
            "startPublicationDate": self._isoformat(offer.publication_date),
            "beginningDate": self._isoformat(offer.beginning_date.value)
            if offer.beginning_date
            else None,
            "locations": [],
        }

    @staticmethod
    def _isoformat(value: Optional[datetime]) -> Optional[str]:
        if not value:
            return None

        naive_value = value.replace(tzinfo=None)
        if not naive_value.microsecond:
            return naive_value.isoformat()

        date_part, _, frac = naive_value.isoformat().partition(".")
        centiseconds = round(int(frac) / 10_000)
        return f"{date_part}.{centiseconds:02d}"

    @staticmethod
    def _coded_object(client_code: str, label: str, type_name: str) -> dict:
        return {
            "code": None,
            "clientCode": client_code,
            "label": label,
            "active": True,
            "parentCode": None,
            "type": type_name,
            "parentType": "",
            "hasChildren": False,
        }


class OfferDetailOutputMapper(OfferSummaryOutputMapper):
    def to_dict(self, offer: Offer) -> dict:
        criteria = offer.criteria

        geolocation = (
            {
                "latitude": offer.localisation.latitude,
                "longitude": offer.localisation.longitude,
            }
            if offer.localisation
            and offer.localisation.latitude is not None
            and offer.localisation.longitude is not None
            else None
        )

        return {
            **super().to_dict(offer),
            "applicationUrl": str(offer.application_url)
            if offer.application_url
            else None,
            "endPublicationDate": None,
            "isAnonymousOrganisation": False,
            "organisation": {
                "entityCode": "",
                "name": offer.organization,
                "description": offer.employer,
                "url": str(offer.offer_url) if offer.offer_url else None,
                "phoneNumber": None,
                "postCode": None,
                "geolocation": geolocation,
                "parentName": None,
                "logoUrl": None,
                "maxDelayForConsent": None,
                "retentionPeriod": None,
                "generalConditions": None,
                "personalDataConsent": None,
            },
            "operationalManager": None,
            "educationLevel": self._coded_object(
                str(criteria.diploma_level.value),
                str(criteria.diploma_level.value),
                "educationLevel",
            )
            if criteria and criteria.diploma_level is not None
            else None,
            "diploma": self._coded_object(criteria.diploma, criteria.diploma, "diploma")
            if criteria and criteria.diploma
            else None,
            "experienceLevel": self._coded_object(
                criteria.experience_level.name,
                criteria.experience_level.value,
                "experienceLevel",
            )
            if criteria and criteria.experience_level
            else None,
            "languages": [self._language(langue) for langue in criteria.languages]
            if criteria
            else [],
            "specialisations": [
                self._coded_object(specialisation, specialisation, "specialisation")
                for specialisation in criteria.specialisations
            ]
            if criteria
            else [],
            "applicationQuestions": [],
            "attachedFilesUrls": [],
            "geolocation": geolocation,
            "customFields": None,
        }

    def _language(self, langue: OfferLanguage) -> dict:
        return {
            "languageName": self._coded_object(
                langue.iso_code, langue.iso_code, "language"
            ),
            "languageLevel": self._coded_object(
                langue.level.name, langue.level.value, "languageLevel"
            ),
        }
