from datetime import datetime, timezone
from uuid import uuid4

from application.ingestion.services.upsert_offers import build_offer
from infrastructure.factories.ingestion.offer_payload_factory import PayloadOfferFactory


def _build(**overrides):
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"}, **overrides
    )
    return build_offer(uuid4(), payload).offer


def test_profession_is_mapped_to_job_family_fields():
    offer = _build(
        profession={"domaine": "NUM", "metier": "ERNUM001", "referentiel": "RMFPv2"}
    )

    assert offer.code_emploi_csp == "ERNUM001"
    assert offer.job_family_referential == "RMFPv2"
    assert offer.functional_area_code == "NUM"


def test_criteres_are_stored_with_every_key():
    offer = _build(
        criteres={
            "diplome_niveau": 5,
            "diplome": "Master",
            "experience": "CONFIRME",
            "specialisations": ["Droit public"],
            "documents_requis": ["CV"],
            "competences_requises": "- Rigueur\n- Autonomie",
            "langues": [{"iso_code": "en", "niveau": "B2"}],
        }
    )

    assert offer.criteria == {
        "diplome_niveau": 5,
        "diplome": "Master",
        "experience": "CONFIRME",
        "specialisations": ["Droit public"],
        "documents_requis": ["CV"],
        "competences_requises": "- Rigueur\n- Autonomie",
        "langues": [{"iso_code": "en", "niveau": "B2"}],
    }


def test_absent_criteres_are_stored_as_none():
    assert _build(criteres=None).criteria is None


def test_export_unif_fields_are_mapped():
    offer = _build(
        description={
            "conditions_exercice": "Télétravail possible",
            "descriptif_service": "Service des ressources humaines",
        },
        publication={
            "fin_publication": datetime(2026, 12, 31, tzinfo=timezone.utc),
            "fin_candidature": datetime(2026, 11, 30, tzinfo=timezone.utc),
            "debut_vacance_poste": datetime(2027, 1, 1, tzinfo=timezone.utc),
        },
    )

    assert offer.exercise_conditions == "Télétravail possible"
    assert offer.service_description == "Service des ressources humaines"
    assert offer.end_publication_date == datetime(2026, 12, 31, tzinfo=timezone.utc)
    assert offer.application_deadline == datetime(2026, 11, 30, tzinfo=timezone.utc)
    assert offer.job_vacancy_date == datetime(2027, 1, 1, tzinfo=timezone.utc)


def test_blank_or_absent_export_unif_fields_are_stored_as_none():
    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        description={"employeur": "", "conditions_exercice": ""},
    )
    del payload["description"]["descriptif_service"]

    offer = build_offer(uuid4(), payload).offer

    assert offer.employer is None
    assert offer.exercise_conditions is None
    assert offer.service_description is None
    assert offer.application_deadline is None
    assert offer.job_vacancy_date is None
