from dataclasses import dataclass, field
from typing import Optional

from referentiel.value_objects.diploma import Diploma
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language_level import LanguageLevel


@dataclass(frozen=True)
class OfferLanguage:
    iso_code: str
    level: LanguageLevel

    def to_dict(self) -> dict:
        return {"iso_code": self.iso_code, "niveau": self.level.name}

    @classmethod
    def from_dict(cls, data: dict) -> "OfferLanguage":
        return cls(iso_code=data["iso_code"], level=LanguageLevel[data["niveau"]])


@dataclass(frozen=True)
class OfferCriteria:
    diploma_level: Optional[Diploma] = None
    diploma: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    specialisations: list[str] = field(default_factory=list)
    documents_requis: list[str] = field(default_factory=list)
    competences_requises: list[str] = field(default_factory=list)
    languages: list[OfferLanguage] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "diplome_niveau": self.diploma_level.value if self.diploma_level else None,
            "diplome": self.diploma,
            "experience": self.experience_level.name if self.experience_level else None,
            "specialisations": self.specialisations,
            "documents_requis": self.documents_requis,
            "competences_requises": self.competences_requises,
            "langues": [langue.to_dict() for langue in self.languages],
        }

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional["OfferCriteria"]:
        if not data:
            return None

        diplome_niveau = data.get("diplome_niveau")
        experience = data.get("experience")

        return cls(
            diploma_level=Diploma(diplome_niveau)
            if diplome_niveau is not None
            else None,
            diploma=data.get("diplome") or None,
            experience_level=ExperienceLevel[experience] if experience else None,
            specialisations=list(data.get("specialisations") or []),
            documents_requis=list(data.get("documents_requis") or []),
            competences_requises=list(data.get("competences_requises") or []),
            languages=[
                OfferLanguage.from_dict(langue) for langue in data.get("langues") or []
            ],
        )
