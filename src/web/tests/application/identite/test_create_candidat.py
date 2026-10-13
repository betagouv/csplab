from unittest.mock import Mock, patch

import pytest
from django.db import IntegrityError
from faker import Faker

from application.identite.services.create_candidat import create_candidat
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.candidat_errors import ProfilCandidatExisteDeja
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.users.models import ProfilCandidatModel, UserModel
from infrastructure.factories.identite.candidat_django_factory import (
    CandidatDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

fake = Faker("fr_FR")


def _candidat_logs(ressource_id):
    return PostgresAuditLogRepository().get_logs_for_ressource("Candidat", ressource_id)


def test_creates_user_and_profile_and_logs(db):
    email = fake.email()

    profil = create_candidat(email=email, prenom="Marie", nom="Martin", resume="CV")

    utilisateur = UserModel.objects.get(username=profil.utilisateur_id)
    assert utilisateur.email == email
    assert utilisateur.first_name == "Marie"
    assert utilisateur.last_name == "Martin"
    assert not utilisateur.has_usable_password()
    assert profil.resume == "CV"
    [log] = _candidat_logs(utilisateur.username)
    assert log.event_name == "ProfilCandidatCree"
    assert log.utilisateur_id == utilisateur.username


def test_stores_the_normalized_email(db):
    profil = create_candidat(
        email="  Marie.MARTIN@GOUV.FR  ",
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    assert profil.utilisateur.email == "marie.martin@gouv.fr"


def test_attaches_profile_to_existing_user_whatever_the_case(db):
    existing = UtilisateurDjangoFactory(
        email="marie.martin@gouv.fr", first_name="Marie", last_name="Martin"
    )

    profil = create_candidat(
        email="Marie.MARTIN@gouv.fr",
        prenom="Autre",
        nom="Nom",
        resume=fake.text(max_nb_chars=200),
    )

    assert profil.utilisateur_id == existing.username
    existing.refresh_from_db()
    assert (existing.first_name, existing.last_name) == ("Marie", "Martin")
    assert UserModel.objects.count() == 1


def test_refuses_a_second_profile_for_the_same_email(db):
    existing = CandidatDjangoFactory()

    with pytest.raises(ProfilCandidatExisteDeja):
        create_candidat(
            email=existing.utilisateur.email,
            prenom=fake.first_name(),
            nom=fake.last_name(),
            resume=fake.text(max_nb_chars=200),
        )

    assert ProfilCandidatModel.objects.count() == 1
    assert UserModel.objects.count() == 1
    assert not AuditLogModel.objects.exists()


def test_reraises_other_integrity_errors(db):
    email = fake.email()

    with pytest.raises(IntegrityError) as excinfo:
        create_candidat(
            email=email,
            prenom=fake.first_name(),
            nom=fake.last_name(),
            resume=None,
        )

    assert "resume" in str(excinfo.value)
    assert not UserModel.objects.filter(email=email).exists()
    assert not AuditLogModel.objects.exists()


@patch.object(
    ProfilCandidatModel,
    "save",
    new=Mock(side_effect=RuntimeError("profile write failed")),
)
def test_rolls_back_user_when_profile_write_fails(db):
    email = fake.email()

    with pytest.raises(RuntimeError):
        create_candidat(
            email=email,
            prenom=fake.first_name(),
            nom=fake.last_name(),
            resume=fake.text(max_nb_chars=200),
        )

    assert not UserModel.objects.filter(email=email).exists()
    assert not AuditLogModel.objects.exists()


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_rolls_back_user_and_profile_when_audit_log_write_fails(db):
    email = fake.email()

    with pytest.raises(RuntimeError):
        create_candidat(
            email=email,
            prenom=fake.first_name(),
            nom=fake.last_name(),
            resume=fake.text(max_nb_chars=200),
        )

    assert not UserModel.objects.filter(email=email).exists()
    assert not ProfilCandidatModel.objects.exists()
