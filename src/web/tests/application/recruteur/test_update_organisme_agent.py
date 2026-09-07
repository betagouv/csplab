from uuid import uuid4

import pytest

from application.recruteur.services.update_organisme_agent import (
    PROFIL_MODIFIE,
    ROLE_MODIFIE,
    update_organisme_agent,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def _organisme_avec_responsable_et_membre(
    prenom="Jeanne", nom="Dupont", poste="Recruteur"
):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    membre = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=AgentOrganismeRole.MEMBRE.value,
        agent__intitule_poste=poste,
        agent__utilisateur__first_name=prenom,
        agent__utilisateur__last_name=nom,
    ).agent
    return responsable, membre, organisme


def _en_tant_que(agent):
    return UtilisateurMapper().to_domain(agent.utilisateur)


def _evenements(agent_id):
    return [
        log.event_name
        for log in PostgresAuditLogRepository().get_logs_for_ressource(
            "AgentOrganisme", agent_id
        )
    ]


def test_responsable_modifie_le_role(db):
    responsable, membre, organisme = _organisme_avec_responsable_et_membre()

    agent_organisme = update_organisme_agent(
        organisme_id=organisme.id,
        agent_id=membre.utilisateur_id,
        utilisateur=_en_tant_que(responsable),
        role=AgentOrganismeRole.RESPONSABLE,
    )

    assert agent_organisme.role == AgentOrganismeRole.RESPONSABLE.value
    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=membre.utilisateur_id
    )
    assert liaison.role == AgentOrganismeRole.RESPONSABLE.value
    assert _evenements(membre.utilisateur_id) == [ROLE_MODIFIE]


def test_responsable_modifie_prenom_nom_et_poste(db):
    responsable, membre, organisme = _organisme_avec_responsable_et_membre()

    agent_organisme = update_organisme_agent(
        organisme_id=organisme.id,
        agent_id=membre.utilisateur_id,
        utilisateur=_en_tant_que(responsable),
        prenom="Camille",
        nom="Martin",
        poste="Directrice des recrutements",
    )

    assert agent_organisme.prenom == "Camille"
    assert agent_organisme.nom == "Martin"
    assert agent_organisme.poste == "Directrice des recrutements"

    compte = UserModel.objects.get(username=membre.utilisateur_id)
    assert (compte.first_name, compte.last_name) == ("Camille", "Martin")
    profil = ProfilAgentModel.objects.get(utilisateur_id=membre.utilisateur_id)
    assert profil.intitule_poste == "Directrice des recrutements"
    assert _evenements(membre.utilisateur_id) == [PROFIL_MODIFIE]


def test_modification_partielle_laisse_les_autres_champs_intacts(db):
    responsable, membre, organisme = _organisme_avec_responsable_et_membre()

    agent_organisme = update_organisme_agent(
        organisme_id=organisme.id,
        agent_id=membre.utilisateur_id,
        utilisateur=_en_tant_que(responsable),
        poste="Chargé de recrutement",
    )

    assert agent_organisme.poste == "Chargé de recrutement"
    assert agent_organisme.prenom == "Jeanne"
    assert agent_organisme.nom == "Dupont"
    assert agent_organisme.role == AgentOrganismeRole.MEMBRE.value


def test_valeurs_identiques_ne_produisent_aucune_trace(db):
    responsable, membre, organisme = _organisme_avec_responsable_et_membre()

    update_organisme_agent(
        organisme_id=organisme.id,
        agent_id=membre.utilisateur_id,
        utilisateur=_en_tant_que(responsable),
        role=AgentOrganismeRole.MEMBRE,
        prenom="Jeanne",
        nom="Dupont",
        poste="Recruteur",
    )

    assert _evenements(membre.utilisateur_id) == []


def test_staff_sans_role_est_autorise(db):
    _, membre, organisme = _organisme_avec_responsable_et_membre()
    staff = UtilisateurDjangoFactory(is_staff=True)

    agent_organisme = update_organisme_agent(
        organisme_id=organisme.id,
        agent_id=membre.utilisateur_id,
        utilisateur=UtilisateurMapper().to_domain(staff),
        role=AgentOrganismeRole.RESPONSABLE,
    )

    assert agent_organisme.role == AgentOrganismeRole.RESPONSABLE.value


def test_membre_est_refuse_et_rien_n_est_ecrit(db):
    _, membre, organisme = _organisme_avec_responsable_et_membre()

    with pytest.raises(AccesOrganismeRefuse):
        update_organisme_agent(
            organisme_id=organisme.id,
            agent_id=membre.utilisateur_id,
            utilisateur=_en_tant_que(membre),
            role=AgentOrganismeRole.RESPONSABLE,
            nom="Martin",
        )

    liaison = OrganismeAgentModel.objects.get(
        organisme_id=organisme.id, agent_id=membre.utilisateur_id
    )
    assert liaison.role == AgentOrganismeRole.MEMBRE.value
    assert UserModel.objects.get(username=membre.utilisateur_id).last_name == "Dupont"
    assert _evenements(membre.utilisateur_id) == []


def test_agent_non_rattache(db):
    responsable, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )
    agent_isole = AgentDjangoFactory()

    with pytest.raises(AgentNonRattache):
        update_organisme_agent(
            organisme_id=organisme.id,
            agent_id=agent_isole.utilisateur_id,
            utilisateur=_en_tant_que(responsable),
            role=AgentOrganismeRole.RESPONSABLE,
        )


def test_organisme_inconnu(db):
    agent_isole = AgentDjangoFactory()

    with pytest.raises(OrganismeNexistePas):
        update_organisme_agent(
            organisme_id=uuid4(),
            agent_id=agent_isole.utilisateur_id,
            utilisateur=UtilisateurMapper().to_domain(UtilisateurDjangoFactory()),
            role=AgentOrganismeRole.MEMBRE,
        )
