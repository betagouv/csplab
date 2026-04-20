from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from domain.entities.document import Document, DocumentType
from tests.factories.talentsoft_factories import TalentsoftOfferFactory
from tests.fixtures.fixture_loader import load_fixture

# Test constants
THREE_DOCUMENTS_COUNT = 3
TWO_DOCUMENTS_COUNT = 2
REFERENCE_YEAR = 2024


def _create_base_document(
    doc_type: DocumentType, doc_id: int, external_id: str, raw_data: Dict[str, Any]
) -> Document:
    return Document(
        external_id=external_id,
        raw_data=raw_data,
        type=doc_type,
        created_at=datetime.now(timezone.utc),
        id=uuid4(),  # Generate UUID automatically
    )


def _load_corps_fixture_data(doc_id: int) -> Dict[str, Any]:
    corps_fixtures = load_fixture("corps_ingres_20251117.json")
    fixture_index = (doc_id - 1) % len(corps_fixtures)
    return corps_fixtures[fixture_index].copy()


def _load_concours_fixture_data(doc_id: int) -> Dict[str, Any]:
    concours_fixtures = load_fixture("concours_greco_2025.json")
    fixture_index = (doc_id - 1) % len(concours_fixtures)
    return concours_fixtures[fixture_index].copy()


def create_test_corps_document(doc_id: int = 1) -> Document:
    raw_data = _load_corps_fixture_data(doc_id)
    return _create_base_document(
        DocumentType.CORPS, doc_id, f"corps_fixture_{doc_id}", raw_data
    )


def create_test_corps_document_fpt(doc_id: int = 1) -> Document:
    raw_data = _load_corps_fixture_data(doc_id)
    raw_data["corpsOuPseudoCorps"]["caracteristiques"]["natureFonctionPublique"][
        "libelleNatureFoncPub"
    ] = "FPT"
    return _create_base_document(
        DocumentType.CORPS, doc_id, f"corps_fpt_fixture_{doc_id}", raw_data
    )


def create_test_corps_document_minarm(doc_id: int = 1) -> Document:
    raw_data = _load_corps_fixture_data(doc_id)
    raw_data["corpsOuPseudoCorps"]["ministereEtInstitutionDeLaRepublique"] = [
        {"libelleMinistere": "MINARM"}
    ]
    return _create_base_document(
        DocumentType.CORPS, doc_id, f"corps_minarm_fixture_{doc_id}", raw_data
    )


def create_test_concours_document(doc_id: int = 1) -> Document:
    raw_data = _load_concours_fixture_data(doc_id)
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_fixture_{doc_id}", raw_data
    )


def create_test_concours_document_invalid_status(doc_id: int = 1) -> Document:
    raw_data = _load_concours_fixture_data(doc_id)
    raw_data["Statut"] = "INVALIDE"
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_invalid_fixture_{doc_id}", raw_data
    )


def create_test_concours_document_old_year(doc_id: int = 1) -> Document:
    raw_data = _load_concours_fixture_data(doc_id)
    raw_data["Année de référence"] = REFERENCE_YEAR
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_old_fixture_{doc_id}", raw_data
    )


def create_test_offer_document(doc_id: int = 1) -> Document:
    offer = TalentsoftOfferFactory.build()
    offer_data = offer.model_dump()

    salary_range_code = (
        offer_data["salaryRange"]["clientCode"]
        if offer_data.get("salaryRange")
        else "UNK"
    )
    external_id = f"{salary_range_code}-{offer_data['reference']}"

    return _create_base_document(DocumentType.OFFERS, doc_id, external_id, offer_data)


def _create_metier_raw_data(doc_id: int) -> Dict[str, Any]:
    return {
        "identifiant": f"FPACH{doc_id:03d}",
        "definitions": {
            "libelles": {
                "libelleCourt": f"Responsable test {doc_id}",
                "libelleLong": f"Responsable test {doc_id}",
            },
            "validite": {
                "status": "A",
                "debutValidite": "2021-09-15T00:00:00Z",
                "finValidite": None,
            },
            "fonctionPublique": {"PFE": "1", "FPT": "1", "FPH": "1"},
            "definitionSynthetiqueDeLEr": {
                "definition": (
                    f"Définir et mettre en oeuvre la politique test {doc_id}"
                    "!N!Manager son équipe!N!Evaluer et suivre la performance."
                )
            },
            "emploiDeReferenceCSP": {
                "codeEmploiCSP": f"ERTEST{doc_id:03d}",
                "libelleEmploiCSP": f"Responsable test {doc_id}",
            },
            "domaineFonctionnel_Famille": {
                "codeDomaineFonctionnel": "TST",
                "libelleDomaineFonctionnel": "Test",
                "codeFamille": "FA0046",
                "libelleFamille": "Encadrement",
            },
        },
        "competences": {
            "activitesDeLEr": [
                {
                    "dateEffet": "2023-08-01T00:00:00Z",
                    "commentaire": (
                        f"Proposer et mettre en oeuvre une organisation test {doc_id}"
                        "!N!Représenter la fonction test!N!Piloter les stratégies test"
                    ),
                }
            ],
            "conditionsParticulieresDExerciceDAcces": [
                {
                    "dateEffet": "2023-08-01T00:00:00Z",
                    "commentaire": f"Condition particulière test {doc_id}",
                }
            ],
            "specificites": {
                "specificitesFPE": None,
                "specificitesFPH": None,
                "specificitesFPT": None,
            },
        },
    }


def create_test_metier_document(doc_id: int = 1) -> Document:
    raw_data = _create_metier_raw_data(doc_id)
    return _create_base_document(
        DocumentType.METIERS, doc_id, f"metier_fixture_{doc_id}", raw_data
    )
