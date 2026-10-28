from referentiel.value_objects.required_document import TALENTSOFT_REQUIRED_DOCUMENTS


def test_talentsoft_required_documents_codes_are_unique():
    codes = [value.client_code for value in TALENTSOFT_REQUIRED_DOCUMENTS]

    assert len(codes) == len(set(codes))


def test_talentsoft_required_documents_combinations_are_unique():
    combinations = [
        frozenset(value.documents) for value in TALENTSOFT_REQUIRED_DOCUMENTS
    ]

    assert len(combinations) == len(set(combinations))
