from dataclasses import dataclass

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur


@dataclass
class LogUtilisateurConnexionInput:
    utilisateur: Utilisateur


class LogUtilisateurConnexionUsecase:
    def __init__(self, audit_log_writer: AuditLogWriter) -> None:
        self._audit_log_writer = audit_log_writer

    def execute(self, input_data: LogUtilisateurConnexionInput) -> None:
        utilisateur = input_data.utilisateur
        self._audit_log_writer.log_action(
            utilisateur_id=utilisateur.entity_id,
            entity=utilisateur,
            ressource_kind=type(utilisateur).__name__,
            event_name="Connexion",
        )
