from infrastructure.factories.seed_recruteur_datas import (
    _AGENTS_SPECS,
    _BRIANCON_UUID,
    _CANDIDATS_SPECS,
    _OFFRES_ACTIVES_SPECS,
    _ORGANISME_UUID,
    _ORGANISMES_SPECS,
)


def _full_name(spec: dict) -> str:
    return f"{spec['prenom']} {spec['nom']}"


AGENT_EMAILS = {spec["prenom"]: spec["email"] for spec in _AGENTS_SPECS}
AGENT_NAMES = {spec["prenom"]: _full_name(spec) for spec in _AGENTS_SPECS}
CANDIDAT_NAMES = {spec["prenom"]: _full_name(spec) for spec in _CANDIDATS_SPECS}
ORGANISME_UUID = _ORGANISME_UUID
BRIANCON_NAME = next(
    spec["nom"] for spec in _ORGANISMES_SPECS if spec["entity_id"] == _BRIANCON_UUID
)
RECRUTEMENT = _OFFRES_ACTIVES_SPECS[1]["title"]
CANDIDAT_FIRST_NAME = "Alice"
CANDIDAT_NAME = CANDIDAT_NAMES[CANDIDAT_FIRST_NAME]
