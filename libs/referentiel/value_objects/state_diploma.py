from dataclasses import dataclass
from typing import Optional

# Talentsoft referential of `customFields.offerCustomBlock1.customCodeTable3`,
# displayed as « Diplômes d'Etat requis » by the BIEP WordPress (see #2287).
# Source: Talentsoft back-office API (scope Customer),
# `GET /api/v1/referentials/customcodetables/_TS_a3e2fd48-425e-4f2a-99c1-ab2ab56f42a8`.
TALENTSOFT_STATE_DIPLOMA_TYPE = "Diplômes d'Etat"


@dataclass(frozen=True)
class TalentsoftStateDiploma:
    client_code: str
    label: str


TALENTSOFT_STATE_DIPLOMAS: tuple[TalentsoftStateDiploma, ...] = tuple(
    TalentsoftStateDiploma(client_code=client_code, label=label)
    for client_code, label in (
        ("CSPU0002", "Diplôme d'Etat d'infirmier"),
        ("CSPU0012", "Diplôme d'Etat d'aide-soignant"),
        ("CASF0001", "Diplôme d'Etat d'éducateur spécialisé"),
        ("CASF0002", "Diplôme d'Etat français d'assistant de service social"),
        ("CSPU0009", "Diplôme d'Etat de masseur-kinésithérapeute"),
        ("DECR0001", "Diplôme d'Etat d'aide médico psychologique"),
        ("CSPU0005", "Diplôme d'Etat d'ergothérapeute"),
        ("CASF0006", "Diplôme d'Etat de moniteur éducateur"),
        ("CEDU0001", "Diplôme d'Etat d'infirmier en pratique avancée"),
        ("CSPU0006", "Diplôme d'Etat de psychomotricien"),
        ("CSPU0013", "Diplôme d'Etat d'auxiliaire de puériculture"),
        ("CSPU0001", "Diplôme d'Etat de sage-femme"),
        ("CEDU0003", "Diplôme d'Etat d'infirmier de bloc opératoire"),
        (
            "CSPO0001",
            "Diplôme d'Etat de la jeunesse, de l'éducation populaire et du sport",
        ),
        ("CASF0003", "Diplôme d'Etat d'éducateur de jeunes enfants"),
        ("CSPU0007", "Diplôme d'Etat de manipulateur d'électroradiologie médicale"),
        ("CSPU0003", "Diplôme d'Etat d'infirmier anesthésiste"),
        ("CSPU0014", "Diplôme d'Etat d'ambulancier"),
        ("CASF0005", "Diplôme d'Etat de conseiller en économie sociale familiale"),
        ("CSPU0004", "Diplôme d'Etat de puéricultrice"),
        ("CSPU0011", "Diplôme d'Etat de technicien de laboratoire médical"),
        ("CASF0004", "Diplôme d'Etat d'éducateur technique spécialisé"),
        ("CSPU0008", "Diplôme d'Etat de pédicure-podologue"),
        # Not used by any offer yet (CEDU0002 and CSPU0015 are duplicates in Talentsoft)
        ("CEDU0002", "Diplôme d'Etat d'audioprothésiste"),
        ("CSPU0010", "Diplôme d'Etat français de diététicien"),
        ("CSPU0015", "Diplôme d'Etat d'audio-protésiste"),
    )
)

_BY_CLIENT_CODE = {d.client_code: d for d in TALENTSOFT_STATE_DIPLOMAS}
_BY_LABEL = {d.label: d for d in TALENTSOFT_STATE_DIPLOMAS}


def talentsoft_state_diploma_by_client_code(
    client_code: Optional[str],
) -> Optional[TalentsoftStateDiploma]:
    return _BY_CLIENT_CODE.get(client_code or "")


def talentsoft_state_diploma_by_label(
    label: Optional[str],
) -> Optional[TalentsoftStateDiploma]:
    return _BY_LABEL.get((label or "").strip())
