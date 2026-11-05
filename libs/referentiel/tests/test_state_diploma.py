from referentiel.value_objects.state_diploma import (
    TALENTSOFT_STATE_DIPLOMAS,
    talentsoft_state_diploma_by_client_code,
    talentsoft_state_diploma_by_label,
)


def test_talentsoft_state_diplomas_has_the_26_codes():
    assert len(TALENTSOFT_STATE_DIPLOMAS) == 26


def test_talentsoft_state_diplomas_codes_are_unique():
    codes = [diploma.client_code for diploma in TALENTSOFT_STATE_DIPLOMAS]

    assert len(codes) == len(set(codes))


def test_talentsoft_state_diplomas_labels_are_unique():
    labels = [diploma.label for diploma in TALENTSOFT_STATE_DIPLOMAS]

    assert len(labels) == len(set(labels))


def test_talentsoft_state_diploma_by_client_code():
    diploma = talentsoft_state_diploma_by_client_code("CSPU0002")

    assert diploma is not None
    assert diploma.label == "Diplôme d'Etat d'infirmier"


def test_talentsoft_state_diploma_by_label_ignores_surrounding_spaces():
    diploma = talentsoft_state_diploma_by_label(" Diplôme d'Etat d'infirmier ")

    assert diploma is not None
    assert diploma.client_code == "CSPU0002"


def test_talentsoft_state_diploma_unknown_values():
    assert talentsoft_state_diploma_by_client_code("Temps_plein") is None
    assert talentsoft_state_diploma_by_client_code(None) is None
    assert talentsoft_state_diploma_by_label("Bac+5 en droit") is None
    assert talentsoft_state_diploma_by_label(None) is None
