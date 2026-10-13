from uuid import uuid4

from ddd.entity import Entity
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.candidat_errors import ProfilCandidatExisteDeja
from domain.identite.value_objects.email import normalize_email
from infrastructure.django_apps.users.models import ProfilCandidatModel, UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def create_candidat(
    *, email: str, prenom: str, nom: str, resume: str
) -> ProfilCandidatModel:
    email = normalize_email(email)
    with transaction.atomic():
        utilisateur, _ = UserModel.objects.get_or_create(
            email=email,
            defaults={
                "username": uuid4(),
                "first_name": prenom,
                "last_name": nom,
                "password": make_password(None),
            },
        )
        try:
            profil = ProfilCandidatModel.objects.create(
                utilisateur=utilisateur, resume=resume
            )
        except IntegrityError as exc:
            if "users_profilcandidatmodel_utilisateur_id_key" in str(exc):
                raise ProfilCandidatExisteDeja(email) from exc
            raise
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=utilisateur.username),
            ressource_kind="Candidat",
            event_name="ProfilCandidatCree",
        )
    return profil
