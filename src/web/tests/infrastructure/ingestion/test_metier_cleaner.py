from unittest.mock import MagicMock

import pytest

from infrastructure.external_gateways.dtos.ingres_metiers_dtos import (
    ConditionsParticulieresDExerciceDAcces,
    DefinitionSynthetiqueDeLEr,
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
