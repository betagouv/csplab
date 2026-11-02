from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from domain.ingestion.entities.document import Document, DocumentType
from infrastructure.external_gateways.dtos.ingres_metiers_dtos import (
    ConditionsParticulieresDExerciceDAcces,
    DefinitionSynthetiqueDeLEr,
    EmploiDeReferenceCSP,
)
from infrastructure.factories.ingestion.ingres_metiers_factories import (
    CompetencesFactory,
    DefinitionsFactory,
    IngresMetiersDocumentFactory,
)
from infrastructure.gateways.ingestion.metier_cleaner import MetierCleaner

DATE_EFFET = "2023-01-01T00:00:00Z"


@pytest.fixture
def cleaner() -> MetierCleaner:
    return MetierCleaner(logger=MagicMock(), metier_repository=MagicMock())


def _make_document(**kwargs):
    return IngresMetiersDocumentFactory.build(**kwargs)


def _definitions_with_description(description: str):
    base = DefinitionsFactory.build()
    return base.model_copy(
        update={
            "definitionSynthetiqueDeLEr": DefinitionSynthetiqueDeLEr(
                definition=description
            )
        }
    )


def _competences_with_conditions(conditions):
    base = CompetencesFactory.build()
    return base.model_copy(
        update={"conditionsParticulieresDExerciceDAcces": conditions}
    )


def test_description_newlines_are_replaced(cleaner):
    document = _make_document(
        definitions=_definitions_with_description(
            "Première ligne.!N!Deuxième ligne.!N!Troisième ligne."
        )
    )

    metier = cleaner._dto_to_entity(document)

    assert metier.description == "Première ligne.\nDeuxième ligne.\nTroisième ligne."


def test_description_without_newline_markers_is_unchanged(cleaner):
    document = _make_document(
        definitions=_definitions_with_description("Description simple sans saut.")
    )

    metier = cleaner._dto_to_entity(document)

    assert metier.description == "Description simple sans saut."


def test_conditions_particulieres_are_split_on_newline_markers(cleaner):
    condition = ConditionsParticulieresDExerciceDAcces(
        dateEffet=DATE_EFFET,
        commentaire="Condition A.!N!Condition B.!N!Condition C.",
    )
    document = _make_document(competences=_competences_with_conditions([condition]))

    metier = cleaner._dto_to_entity(document)

    assert metier.conditions_particulieres == [
        "Condition A.",
        "Condition B.",
        "Condition C.",
    ]


def test_conditions_particulieres_multiple_entries_are_flattened(cleaner):
    conditions = [
        ConditionsParticulieresDExerciceDAcces(
            dateEffet=DATE_EFFET,
            commentaire="Condition A.!N!Condition B.",
        ),
        ConditionsParticulieresDExerciceDAcces(
            dateEffet=DATE_EFFET,
            commentaire="Condition C.",
        ),
    ]
    document = _make_document(competences=_competences_with_conditions(conditions))

    metier = cleaner._dto_to_entity(document)

    assert metier.conditions_particulieres == [
        "Condition A.",
        "Condition B.",
        "Condition C.",
    ]


def test_conditions_particulieres_empty_when_none(cleaner):
    document = _make_document(competences=_competences_with_conditions(None))

    metier = cleaner._dto_to_entity(document)

    assert metier.conditions_particulieres == []


def _raw_document(document) -> Document:
    return Document(
        entity_id=uuid4(),
        raw_data=document.model_dump(),
        type=DocumentType.METIERS,
        created_at=datetime.now(),
    )


def test_offer_family_code_comes_from_code_emploi_csp(cleaner):
    document = _make_document()

    metier = cleaner._dto_to_entity(document)

    assert metier.offer_family_code == "ERACH001"


@pytest.mark.parametrize("code_emploi_csp", [None, ""])
def test_metier_without_code_emploi_csp_is_rejected(cleaner, code_emploi_csp):
    definitions = DefinitionsFactory.build().model_copy(
        update={
            "emploiDeReferenceCSP": EmploiDeReferenceCSP(codeEmploiCSP=code_emploi_csp)
        }
    )
    rejected = _make_document(identifiant="FPDIR016", definitions=definitions)
    kept = _make_document(identifiant="FPACH001")

    result = cleaner.clean([_raw_document(rejected), _raw_document(kept)])

    assert [m.external_id for m in result.entities] == ["FPACH001"]
    assert len(result.cleaning_errors) == 1
    assert "FPDIR016" in result.cleaning_errors[0]["error"]
    assert "codeEmploiCSP" in result.cleaning_errors[0]["error"]
