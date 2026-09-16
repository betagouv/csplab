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

MIXTE = "  Jean.DUPONT@GOUV.FR  "
ATTENDU = "jean.dupont@gouv.fr"


class TestUserModelSave:
    def test_met_l_email_en_minuscules(self, db):
        user = UserModel.objects.create(username=uuid4(), email=MIXTE)

        user.refresh_from_db()
        assert user.email == ATTENDU

    def test_normalise_aussi_a_la_mise_a_jour(self, db):
        user = UtilisateurDjangoFactory(email="initial@gouv.fr")

        user.email = "AUTRE@Gouv.FR"
        user.save()

        user.refresh_from_db()
        assert user.email == "autre@gouv.fr"

    def test_le_doublon_de_casse_est_refuse(self, db):
        UtilisateurDjangoFactory(email=ATTENDU)

        # unique=True est sensible a la casse, mais save() ayant normalise, les
        # deux valeurs se rejoignent et le doublon est bloque.
        with pytest.raises(IntegrityError), transaction.atomic():
            UserModel.objects.create(username=uuid4(), email=MIXTE)


class TestRechercheParEmail:
    @pytest.fixture(name="agent")
    def agent_fixture(self, db):
        return AgentDjangoFactory(utilisateur__email=ATTENDU)

    def test_par_email_trouve_quelle_que_soit_la_casse(self, agent):
        assert ProfilAgentModel.objects.par_email(MIXTE).first() == agent

    def test_repository_agent_trouve_quelle_que_soit_la_casse(self, agent):
        assert PostgresAgentRepository().get_by_email(MIXTE) is not None

    def test_repository_utilisateur_trouve_quelle_que_soit_la_casse(self, agent):
        utilisateur = PostgresUtilisateurRepository().get_by_email(MIXTE)

        assert utilisateur.email == ATTENDU


class TestContrainteUniqueInsensibleALaCasse:
    def test_bloque_un_doublon_ecrit_sans_passer_par_save(self, db):
        UtilisateurDjangoFactory(email=ATTENDU)
        autre = UtilisateurDjangoFactory(email="autre@gouv.fr")

        # update() court-circuite save(), donc la normalisation applicative. Si
        # le test passe, c'est la base qui refuse, pas le code Python.
        with pytest.raises(IntegrityError), transaction.atomic():
            UserModel.objects.filter(pk=autre.pk).update(email="JEAN.DUPONT@GOUV.FR")

    def test_laisse_passer_deux_emails_reellement_differents(self, db):
        UtilisateurDjangoFactory(email=ATTENDU)
        autre = UtilisateurDjangoFactory(email="autre@gouv.fr")

        UserModel.objects.filter(pk=autre.pk).update(email="AUTRE.ADRESSE@GOUV.FR")

        autre.refresh_from_db()
        assert autre.email == "AUTRE.ADRESSE@GOUV.FR"
