"""Shared factory functions and constants for clean documents tests."""

from datetime import datetime
from typing import Any, Dict

from domain.entities.document import Document, DocumentType
from tests.fixtures.fixture_loader import load_fixture

# Test constants
MULTIPLE_DOCUMENTS_COUNT = 3
MIXED_DOCUMENTS_CLEANED = 2
REFERENCE_YEAR = 2024


def _create_base_document(
    doc_type: DocumentType, doc_id: int, external_id: str, raw_data: Dict[str, Any]
) -> Document:
    """Helper to create a Document instance with common fields."""
    return Document(
        id=doc_id,
        external_id=external_id,
        raw_data=raw_data,
        type=doc_type,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def _load_corps_fixture_data(doc_id: int) -> Dict[str, Any]:
    """Load and return corps fixture data for given doc_id."""
    corps_fixtures = load_fixture("corps_ingres_20251117.json")
    fixture_index = (doc_id - 1) % len(corps_fixtures)
    return corps_fixtures[fixture_index].copy()


def _load_concours_fixture_data(doc_id: int) -> Dict[str, Any]:
    """Load and return concours fixture data for given doc_id."""
    concours_fixtures = load_fixture("concours_greco_2025.json")
    fixture_index = (doc_id - 1) % len(concours_fixtures)
    return concours_fixtures[fixture_index].copy()


def _load_offer_fixture_data(doc_id: int) -> Dict[str, Any]:
    """Load and return offer fixture data for given doc_id."""
    offer_fixtures = load_fixture("offers_talentsoft_20260124.json")
    fixture_index = (doc_id - 1) % len(offer_fixtures)
    return offer_fixtures[fixture_index].copy()

def create_test_corps_document(doc_id: int = 1) -> Document:
    """Create a test CORPS document using real fixture data."""
    raw_data = _load_corps_fixture_data(doc_id)
    return _create_base_document(
        DocumentType.CORPS, doc_id, f"corps_fixture_{doc_id}", raw_data
    )


def create_test_corps_document_fpt(doc_id: int = 1) -> Document:
    """Create a test CORPS document with FPT using fixture data."""
    raw_data = _load_corps_fixture_data(doc_id)
    raw_data["corpsOuPseudoCorps"]["caracteristiques"]["natureFonctionPublique"][
        "libelleNatureFoncPub"
    ] = "FPT"
    return _create_base_document(
        DocumentType.CORPS, doc_id, f"corps_fpt_fixture_{doc_id}", raw_data
    )


def create_test_corps_document_minarm(doc_id: int = 1) -> Document:
    """Create a test CORPS document with MINARM ministry using fixture data."""
    raw_data = _load_corps_fixture_data(doc_id)
    raw_data["corpsOuPseudoCorps"]["ministereEtInstitutionDeLaRepublique"] = [
        {"libelleMinistere": "MINARM"}
    ]
    return _create_base_document(
        DocumentType.CORPS, doc_id, f"corps_minarm_fixture_{doc_id}", raw_data
    )


def create_test_concours_document(doc_id: int = 1) -> Document:
    """Create a test CONCOURS document using real fixture data."""
    raw_data = _load_concours_fixture_data(doc_id)
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_fixture_{doc_id}", raw_data
    )


def create_test_concours_document_invalid_status(doc_id: int = 1) -> Document:
    """Create a test CONCOURS document with invalid status using fixture data."""
    raw_data = _load_concours_fixture_data(doc_id)
    raw_data["Statut"] = "INVALIDE"
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_invalid_fixture_{doc_id}", raw_data
    )


def create_test_concours_document_old_year(doc_id: int = 1) -> Document:
    """Create a test CONCOURS document with old year using fixture data."""
    raw_data = _load_concours_fixture_data(doc_id)
    raw_data["Année de référence"] = REFERENCE_YEAR
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_old_fixture_{doc_id}", raw_data
    )


def create_test_offer_document(doc_id: int = 1) -> Document:
    """Create a test OFFER document using real TalentSoft fixture data."""
    offer_data = _load_offer_fixture_data(doc_id)

    # Ensure unique reference for each document to avoid conflicts
    original_reference = offer_data["reference"]
    offer_data["reference"] = f"{original_reference}-{doc_id}"

    # Use the offer data directly (not wrapped in API response)
    return _create_base_document(
        DocumentType.OFFERS, doc_id, f"offer_fixture_{doc_id}", offer_data
    )


def create_test_offer_document_missing_required(doc_id: int = 1) -> Document:
    """Create a test OFFERS document with missing required fields."""
    offer_data = _load_offer_fixture_data(doc_id)

    # Remove required fields to test validation
    del offer_data["title"]  # Missing required field
    offer_data["organisationName"] = ""  # Empty required field

    return _create_base_document(
        DocumentType.OFFERS, doc_id, f"offer_missing_required_{doc_id}", offer_data
    )


def create_test_offer_document_invalid_types(doc_id: int = 1) -> Document:
    """Create a test OFFERS document with invalid field types."""
    offer_data = _load_offer_fixture_data(doc_id)

    # Invalid types to test validation
    offer_data["isTopOffer"] = "not_a_boolean"  # Should be boolean
    offer_data["offerFamilyCategory"]["code"] = "not_an_int"  # Should be int
    if offer_data.get("latitude"):
        offer_data["latitude"] = "not_a_float"  # Should be float

    return _create_base_document(
        DocumentType.OFFERS, doc_id, f"offer_invalid_types_{doc_id}", offer_data
    )


def create_test_offer_document_invalid_structure(doc_id: int = 1) -> Document:
    """Create a test OFFERS document with invalid structure."""
    # Invalid structure - missing required fields completely
    raw_data = {
        "invalid_field": "invalid_value",
        "missing_reference": True,
    }

    return _create_base_document(
        DocumentType.OFFERS, doc_id, f"offer_invalid_structure_{doc_id}", raw_data
    )
    raw_data["Année de référence"] = REFERENCE_YEAR  # Old year
    return _create_base_document(
        DocumentType.CONCOURS, doc_id, f"concours_old_fixture_{doc_id}", raw_data
    )
