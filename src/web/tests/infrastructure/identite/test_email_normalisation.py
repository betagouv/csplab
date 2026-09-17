from uuid import uuid4

import pytest
from django.db import IntegrityError, transaction

from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.repositories.identite.postgres_agent_repository import (
    PostgresAgentRepository,
)
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)

MIXED_CASE = "  Jean.DUPONT@GOUV.FR  "
EXPECTED = "jean.dupont@gouv.fr"


class TestUserModelSave:
    def test_lowercases_the_email(self, db):
        user = UserModel.objects.create(username=uuid4(), email=MIXED_CASE)

        user.refresh_from_db()
        assert user.email == EXPECTED

    def test_lowercases_on_update_too(self, db):
        user = UtilisateurDjangoFactory(email="initial@gouv.fr")

        user.email = "AUTRE@Gouv.FR"
        user.save()

        user.refresh_from_db()
        assert user.email == "autre@gouv.fr"

    def test_rejects_a_case_variant_duplicate(self, db):
        UtilisateurDjangoFactory(email=EXPECTED)

        with pytest.raises(IntegrityError), transaction.atomic():
            UserModel.objects.create(username=uuid4(), email=MIXED_CASE)


class TestSearchByEmail:
    @pytest.fixture(name="agent")
    def agent_fixture(self, db):
        return AgentDjangoFactory(utilisateur__email=EXPECTED)

    def test_par_email_finds_whatever_the_case(self, agent):
        assert ProfilAgentModel.objects.par_email(MIXED_CASE).first() == agent

    def test_agent_repository_finds_whatever_the_case(self, agent):
        assert PostgresAgentRepository().get_by_email(MIXED_CASE) is not None

    def test_utilisateur_repository_finds_whatever_the_case(self, agent):
        utilisateur = PostgresUtilisateurRepository().get_by_email(MIXED_CASE)

        assert utilisateur.email == EXPECTED


class TestLowercaseCheckConstraint:
    def test_rejects_a_write_that_bypasses_save(self, db):
        user = UtilisateurDjangoFactory(email="autre@gouv.fr")

        with pytest.raises(IntegrityError), transaction.atomic():
            UserModel.objects.filter(pk=user.pk).update(email="AUTRE@GOUV.FR")

    def test_rejects_a_padded_write_that_bypasses_save(self, db):
        user = UtilisateurDjangoFactory(email="autre@gouv.fr")

        with pytest.raises(IntegrityError), transaction.atomic():
            UserModel.objects.filter(pk=user.pk).update(email="  autre@gouv.fr  ")

    def test_accepts_a_lowercase_write_that_bypasses_save(self, db):
        user = UtilisateurDjangoFactory(email="autre@gouv.fr")

        UserModel.objects.filter(pk=user.pk).update(email="nouvelle.adresse@gouv.fr")

        user.refresh_from_db()
        assert user.email == "nouvelle.adresse@gouv.fr"
