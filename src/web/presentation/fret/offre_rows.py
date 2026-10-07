import gettext
import json
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any

import pycountry
from django.db import models
from django.template.defaultfilters import linebreaksbr
from django.utils.html import format_html, format_html_join
from django.utils.safestring import SafeString
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_kind import ContractKind
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import (
    Management,
    OpenToMilitary,
    WorkingPlace,
    WorkingTime,
)
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.offer import OfferModel

_LABELS = {
    "reference": "Référence",
    "title": "Titre",
    "long_title": "Titre long",
    "organization": "Organisme",
    "employer": "Employeur",
    "verse": "Versant",
    "category": "Catégorie",
    "offer_nature": "Nature de l'offre",
    "contract_kind": "Type de contrat",
    "job_vacancy": "Poste vacant",
    "area": "Zone géographique",
    "country": "Pays",
    "region": "Région",
    "department": "Département",
    "location_label": "Localisation",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "publication_date": "Date de publication",
    "beginning_date": "Date de début",
    "application_deadline": "Date limite de candidature",
    "offer_url": "Lien de l'offre",
    "application_url": "Lien de candidature",
    "code_emploi_csp": "Code emploi CSP",
    "job_family_referential": "Référentiel de familles de métiers",
    "functional_area_code": "Code du domaine fonctionnel",
    "local_job_code": "Code du métier local",
    "service_description": "Description du service",
    "exercise_conditions": "Conditions d'exercice",
    "complements": "Compléments",
    "criteria": "Critères",
    "conditions": "Conditions",
    "contacts": "Contacts",
    "talentsoft_organisme_entity_code": "Organisme Talentsoft",
    "processing": "En cours de traitement",
    "processed_at": "Traitée le",
    "archived_at": "Archivée le",
    "created_at": "Créée le",
    "updated_at": "Mise à jour le",
}
_HIDDEN = {"id", "source", "mission", "profile"}
_ENUM_LABELS = {
    "verse": lambda value: Verse(value).label,
    "category": lambda value: Category(value).label,
    "offer_nature": lambda value: OfferNature(value).label,
    "contract_kind": lambda value: ContractKind[value].label,
}
_DATETIME_FORMAT = "%d/%m/%Y %H:%M"
_NOT_PROVIDED = format_html("<em>{}</em>", "Non renseigné")


def _is_empty(value: Any) -> bool:
    return value is None or value in ("", [], {})


def _humanize(field: models.Field, value: Any) -> Any:
    if field.name in _ENUM_LABELS:
        try:
            return _ENUM_LABELS[field.name](value)
        except (KeyError, ValueError):
            return value  # valeur inconnue des enums : on l'affiche telle quelle
    if isinstance(value, bool):
        return "Oui" if value else "Non"
    if isinstance(value, datetime):
        return value.strftime(_DATETIME_FORMAT)
    return value


def _format(field: models.Field, value: Any) -> SafeString:
    value = _humanize(field, value)
    if isinstance(field, models.URLField):
        return format_html(
            '<a href="{0}" rel="noopener" target="_blank">{0}</a>', value
        )
    if field.name == "contacts" and isinstance(value, list):
        return _contacts(value)
    if isinstance(value, dict | list):
        dumped = json.dumps(value, ensure_ascii=False, indent=2)
        return format_html("<pre>{}</pre>", dumped)
    if isinstance(value, str):
        return linebreaksbr(value)
    return format_html("{}", value)


_fr_language_names = gettext.translation(
    "iso639-3", pycountry.LOCALES_DIR, languages=["fr"], fallback=True
).gettext


def _enum_label(enum: type[Enum], value: Any) -> str:
    """Libellé d'un membre retrouvé par son nom, sinon par sa valeur."""
    for lookup in (lambda: enum[value], lambda: enum(value)):
        try:
            return lookup().label  # type: ignore[attr-defined]
        except (KeyError, ValueError):
            continue
    return str(value)


def _date(value: Any) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        return str(value)


def _language_name(iso_code: str) -> str:
    language = pycountry.languages.get(alpha_2=str(iso_code).lower())
    return _fr_language_names(language.name) if language else str(iso_code)


def _languages(languages: list[dict]) -> str:
    return ", ".join(
        f"{_language_name(langue.get('iso_code', ''))} ({langue.get('niveau', '')})"
        for langue in languages
    )


def _link(url: str) -> SafeString:
    return format_html('<a href="{0}" rel="noopener" target="_blank">{0}</a>', url)


def _contacts(contacts: list) -> SafeString:
    """Adresses de contact, séparées par des virgules, avec un lien `mailto:`."""
    return format_html_join(
        ", ",
        '<a href="mailto:{0}">{0}</a>',
        (
            (contact["email"],)
            for contact in contacts
            if isinstance(contact, dict) and contact.get("email")
        ),
    )


def _enum(enum: type[Enum]) -> Callable[[Any], str]:
    return lambda value: _enum_label(enum, value)


def _text_list(values: list) -> str:
    return ", ".join(str(value) for value in values)


# (clé du JSON, libellé, mise en forme de la valeur) pour les colonnes JSON de l'offre.
_CRITERIA = [
    ("diplome_niveau", "Niveau de diplôme", lambda value: f"Niveau {value}"),
    ("diplome", "Diplôme", None),
    ("experience", "Niveau d'expérience", _enum(ExperienceLevel)),
    ("specialisations", "Spécialisations", _text_list),
    ("documents_requis", "Documents requis", _text_list),
    ("competences_requises", "Compétences requises", _text_list),
    ("langues", "Langues", _languages),
]
_CONDITIONS = [
    ("salaire_titulaire", "Salaire (titulaire)", None),
    ("salaire_contractuel", "Salaire (contractuel)", None),
    ("debut_contrat", "Début du contrat", _date),
    ("fin_contrat", "Fin du contrat", _date),
    ("duree_contrat", "Durée du contrat", None),
    ("temps_travail", "Temps de travail", _enum(WorkingTime)),
    ("ouvert_aux_militaires", "Ouvert aux militaires", _enum(OpenToMilitary)),
    ("lieu_de_travail", "Lieu de travail", _enum(WorkingPlace)),
    ("management", "Management", _enum(Management)),
    ("complements", "Compléments", None),
    ("bases_legales", "Bases légales", None),
    ("note_ouverture_poste_url", "Note d'ouverture du poste", _link),
]
_JSON_GROUPS = {
    "criteria": ("Critères", _CRITERIA),
    "conditions": ("Conditions", _CONDITIONS),
}


def _group_rows(group: str, specs: list, data: dict | None) -> list[list[SafeString]]:
    """Une ligne par clé connue du JSON, renseignée ou non."""
    rows = []
    for key, label, formatter in specs:
        value = (data or {}).get(key)
        if _is_empty(value):
            cell = _NOT_PROVIDED
        else:
            shown = formatter(value) if formatter else value
            cell = shown if isinstance(shown, SafeString) else linebreaksbr(shown)
        rows.append([format_html("<strong>{} — {}</strong>", group, label), cell])
    return rows


def _value(offre: OfferModel, field: models.Field) -> Any:
    if field.name == "talentsoft_organisme_entity_code":
        organisme = offre.talentsoft_organisme_entity_code
        return organisme and f"{organisme.name} ({organisme.entity_code})"
    return getattr(offre, field.attname)


def offre_rows(offre: OfferModel) -> list[list[SafeString]]:
    fields = {field.name: field for field in offre._meta.concrete_fields}
    ordered = [name for name in _LABELS if name in fields]
    ordered += [name for name in fields if name not in _LABELS and name not in _HIDDEN]
    rows = []
    for name in ordered:
        field = fields[name]
        value = _value(offre, field)
        if name in _JSON_GROUPS:
            group, specs = _JSON_GROUPS[name]
            rows += _group_rows(group, specs, value)
            continue
        label = _LABELS.get(name, name)
        rows.append(
            [
                format_html("<strong>{}</strong>", label),
                _NOT_PROVIDED if _is_empty(value) else _format(field, value),
            ]
        )
    return rows
