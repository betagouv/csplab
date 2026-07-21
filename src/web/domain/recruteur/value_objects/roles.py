from enum import Enum


class AgentOrganismeRole(Enum):
    RESPONSABLE = "responsable"
    MEMBRE = "membre"


class AgentRecrutementRole(Enum):
    RESPONSABLE = "responsable"
    RECRUTEUR = "recruteur"
    CONTRIBUTEUR = "contributeur"
