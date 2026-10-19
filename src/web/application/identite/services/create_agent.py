from uuid import UUID, uuid4

from ddd.entity import Entity
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.identite.value_objects.email import normalize_email
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def create_agent(
    *, email: str, organisme_id: UUID, utilisateur: UserModel
) -> ProfilAgentModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.CREATE_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    email = normalize_email(email)
    with transaction.atomic():
        agent_utilisateur, _ = UserModel.objects.get_or_create(
            email=email,
            defaults={"username": uuid4(), "password": make_password(None)},
        )
        try:
            profil = ProfilAgentModel.objects.create(utilisateur=agent_utilisateur)
        except IntegrityError as exc:
            if "users_profilagentmodel_utilisateur_id_key" in str(exc):
                raise ProfilAgentExisteDeja(email) from exc
            raise
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=agent_utilisateur.username),
            ressource_kind="Agent",
            event_name="ProfilAgentCree",
        )
    return profil
