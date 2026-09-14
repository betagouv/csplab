from enum import Enum


class AgentOrganismeRole(Enum):
    SUPERVISEUR = "responsable"
    AGENT = "membre"


class AgentRecrutementRole(Enum):
    RESPONSABLE = "responsable"
    RECRUTEUR = "recruteur"
    CONTRIBUTEUR = "contributeur"
