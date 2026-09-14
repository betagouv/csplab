from enum import Enum


class AgentOrganismeRole(Enum):
    SUPERVISEUR = "superviseur"
    AGENT = "agent"


class AgentRecrutementRole(Enum):
    RESPONSABLE = "responsable"
    RECRUTEUR = "recruteur"
    CONTRIBUTEUR = "contributeur"
