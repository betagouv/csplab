import pytest

from referentiel.value_objects.offer_criteria import OfferCriteria
from referentiel.value_objects.required_document import RequiredDocument


def test_required_documents_are_stored_by_name():
    criteria = OfferCriteria(
        documents_requis=[RequiredDocument.CV, RequiredDocument.LETTRE_MOTIVATION]
    )

    assert criteria.to_dict()["documents_requis"] == ["CV", "LETTRE_MOTIVATION"]


def test_required_documents_are_read_from_their_name():
    criteria = OfferCriteria.from_dict({"documents_requis": ["CV", "PORTFOLIO"]})

    assert criteria is not None
    assert criteria.documents_requis == [
        RequiredDocument.CV,
        RequiredDocument.PORTFOLIO,
    ]


def test_unknown_required_document_raises():
    with pytest.raises(KeyError):
        OfferCriteria.from_dict({"documents_requis": ["Copie des diplômes"]})


@pytest.mark.parametrize(
    "stored,expected",
    [
        ("- Rigueur", "- Rigueur"),
        (["Rigueur", "Autonomie"], "Rigueur\nAutonomie"),
        ([], None),
        ("", None),
        (None, None),
    ],
    ids=["markdown", "legacy-list", "legacy-empty-list", "blank", "null"],
)
def test_required_skills_are_read_as_markdown(stored, expected):
    criteria = OfferCriteria.from_dict({"competences_requises": stored})

    assert criteria is not None
    assert criteria.competences_requises == expected
