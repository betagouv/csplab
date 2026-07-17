from enum import StrEnum


class LoggerName(StrEnum):
    DJANGO = "django"
    WEB = "web"
    CANDIDATE = "candidate"
    INGESTION = "ingestion"
    IDENTITE = "identite"
    RECRUTEUR = "recruteur"
