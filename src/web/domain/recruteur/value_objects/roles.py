from enum import Enum


class AgentOrganismeRole(Enum):
    SUPERVISEUR = "superviseur"
    MEMBRE = "membre"


class AgentRecrutementRole(Enum):
    RESPONSABLE = "responsable"
    RECRUTEUR = "recruteur"
    CONTRIBUTEUR = "contributeur"
