from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, HttpUrl, model_serializer
from referentiel.value_objects.language import Language

from domain.entities.offer import Offer


class IdentificationPayload(BaseModel):
    reference: str
    source: str
    versant: Optional[str]


class OrganisationPayload(BaseModel):
    nom: str
    siret: str = ""


class ProfessionPayload(BaseModel):
    domaine: str
    metier: str


class DescriptionPayload(BaseModel):
    mission: str
    profil: str
    employeur: str
    complements: str = ""


class LocalisationItemPayload(BaseModel):
    zone_geographique: str
    pays: str
    region: str
    departement: str
    localisation_label: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PublicationPayload(BaseModel):
    debut_publication: datetime
    fin_publication: datetime


class LanguagePayload(BaseModel):
    iso_code: str
    niveau: str

    @classmethod
    def from_language(cls, language: Language) -> LanguagePayload:
        return cls(iso_code=language.iso_code, niveau=str(language.language_level))


class CriteresPayload(BaseModel):
    diplome_niveau: Optional[int] = None
    experience: Optional[str] = None
    diploma: Optional[str] = None
    specialisations: list[str] = []
    languages: list[LanguagePayload] = []

    @model_serializer
    def serialize(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None and v != []}


class OfferUpsertPayload(BaseModel):
    identification: IdentificationPayload
    titre: str
    titre_long: str
    organisation: OrganisationPayload
    url_offre: Optional[HttpUrl] = None
    url_candidature: Optional[HttpUrl] = None
    profession: ProfessionPayload
    categories: list[str] = []
    type_contrat: Optional[str] = None
    forme_contrat: list[str] = []
    vacance_poste: str = ""
    description: DescriptionPayload
    localisation: Optional[list[LocalisationItemPayload]] = None
    criteres: Optional[CriteresPayload] = None
    conditions: None = None
    contacts: None = None
    publication: PublicationPayload

    @classmethod
    def from_offer(cls, offer: Offer) -> OfferUpsertPayload:
        fin_publication = (
            offer.end_publication_date
            or (offer.beginning_date.value if offer.beginning_date else None)
            or offer.publication_date + timedelta(days=365)
        )

        localisation = None
        if offer.localisation:
            localisation = [
                LocalisationItemPayload(
                    zone_geographique=offer.localisation.area.value,
                    pays=str(offer.localisation.country),
                    region=offer.localisation.region.code,
                    departement=offer.localisation.department.code,
                )
            ]

        domaine_length = 3
        domaine = (
            offer.family_code[:domaine_length]
            if offer.family_code and len(offer.family_code) >= domaine_length
            else ""
        )

        return cls(
            identification=IdentificationPayload(
                reference=offer.reference,
                source=str(offer.source_id),
                versant=offer.verse.value if offer.verse else None,
            ),
            titre=offer.title,
            titre_long=offer.title,
            organisation=OrganisationPayload(nom=offer.organization),
            url_offre=offer.offer_url,
            url_candidature=offer.application_url,
            profession=ProfessionPayload(
                domaine=domaine,
                metier=offer.family_code or "",
            ),
            categories=[offer.category.value] if offer.category else [],
            type_contrat=offer.contract_type.value if offer.contract_type else None,
            description=DescriptionPayload(
                mission=offer.mission,
                profil=offer.profile,
                employeur=offer.organization,
            ),
            localisation=localisation,
            criteres=CriteresPayload(
                diplome_niveau=offer.education_level,
                experience=offer.experience.name if offer.experience else None,
                diploma=offer.diploma,
                specialisations=offer.specialisations,
                languages=[
                    LanguagePayload.from_language(lang) for lang in offer.languages
                ],
            )
            if offer.education_level
            or offer.experience
            or offer.diploma
            or offer.specialisations
            or offer.languages
            else None,
            publication=PublicationPayload(
                debut_publication=offer.publication_date,
                fin_publication=fin_publication,
            ),
        )
