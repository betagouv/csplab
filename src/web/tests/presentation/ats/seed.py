from infrastructure.factories.seed_recruteur_datas import (
    _AGENTS_SPECS,
    _CANDIDATS_SPECS,
    _ORGANISME_UUID,
)


def _full_name(spec: dict) -> str:
    return f"{spec['prenom']} {spec['nom']}"


AGENT_EMAILS = {spec["prenom"]: spec["email"] for spec in _AGENTS_SPECS}
ORGANISME_UUID = _ORGANISME_UUID
SUPERVISEUR = "Marie"
RECRUTEMENT = "Responsable RH"
CANDIDAT_FIRST_NAME = "Alice"
CANDIDAT_NAME = next(
    _full_name(spec)
    for spec in _CANDIDATS_SPECS
    if spec["prenom"] == CANDIDAT_FIRST_NAME
)
