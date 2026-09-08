from uuid import UUID, uuid4

import pytest

from application.recruteur.usecases.changer_etape_candidatures import (
    ChangerEtapeCandidaturesCommand,
)
from config.app_config import AppConfig
from domain.identite.errors.organisme_permission_errors import (
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.exceptions.exceptions import InfrastructureError
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from infrastructure.gateways.shared.logger import LoggerService


# transactional_db to test integrity constraints
@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(transactional_db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="recrutement_mapper")
def recrutement_mapper_fixture(recruteur_integration_container):
    return recruteur_integration_container.recrutement_mapper()


@pytest.fixture(name="usecase")
def usecase_fixture(recruteur_integration_container):
    return recruteur_integration_container.changer_etape_candidatures_usecase()


class TestChangerEtapeCandidaturesUsecase:
    @pytest.mark.parametrize(
        ("role_organisme", "role_recrutement"),
        [
            pytest.param(
                AgentOrganismeRole.RESPONSABLE,
                AgentRecrutementRole.RESPONSABLE,
                id="gestionnaire_responsable",
            ),
            pytest.param(
                AgentOrganismeRole.RESPONSABLE,
                AgentRecrutementRole.CONTRIBUTEUR,
                id="gestionnaire_contributeur",
            ),
            pytest.param(
                AgentOrganismeRole.MEMBRE,
                AgentRecrutementRole.RESPONSABLE,
                id="membre_responsable",
            ),
            pytest.param(
                AgentOrganismeRole.MEMBRE,
                AgentRecrutementRole.RECRUTEUR,
                id="membre_recruteur",
            ),
        ],
    )
    def test_authorized(
        self,
        usecase,
        role_organisme,
        role_recrutement,
    ):
        agent, organisme = create_organisme_with_agent(role=role_organisme)
        agent_id = agent.utilisateur_id
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            agent_link__agent=agent,
            agent_link__role=role_recrutement.value,
        )
        etape_entree = EtapeModel.objects.get(
            recrutement_id=recrutement.offre_id,
            categorie=CategorieEtapeRecrutement.ENTREE.value,
        )
        candidatures = CandidatureDjangoFactory.create_batch(3, etape=etape_entree)
        etape_cible_id = UUID(recrutement.ordre_etapes[-1])

        command = ChangerEtapeCandidaturesCommand(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.offre_id,
            utilisateur=UtilisateurFactory.create_entity(entity_id=agent_id),
            etape_cible_id=etape_cible_id,
            candidatures=[candidature.id for candidature in candidatures],
        )

        resultat = usecase.execute(command)

        assert all(c.etape_id == etape_cible_id for c in resultat["successes"])

        assert resultat["failures"] == []

    def test_unauthorized(
        self,
        usecase,
    ):
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        agent_id = agent.utilisateur_id
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        etape_entree = EtapeModel.objects.get(
            recrutement_id=recrutement.offre_id,
            categorie=CategorieEtapeRecrutement.ENTREE.value,
        )
        candidatures = CandidatureDjangoFactory.create_batch(3, etape=etape_entree)

        command = ChangerEtapeCandidaturesCommand(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.offre_id,
            utilisateur=UtilisateurFactory.create_entity(entity_id=agent_id),
            etape_cible_id=uuid4(),
            candidatures=[candidature.id for candidature in candidatures],
        )

        with pytest.raises(AccesRecrutementRefuse):
            usecase.execute(command)

    def test_candidature_inexistante(self, recrutement_mapper, usecase):
        agent_model = AgentDjangoFactory()

        recrutement_model = RecrutementDjangoFactory()
        recrutement = recrutement_mapper.to_domain(recrutement_model)
        etape_cible_id = recrutement.etapes[-1].entity_id

        unknown_candidature_ids = [uuid4(), uuid4()]

        OrganismeAgentModel(
            id=uuid4(),
            organisme_id=recrutement.organisme_id,
            agent_id=agent_model.utilisateur_id,
            role=AgentOrganismeRole.RESPONSABLE.value,
        ).save()

        with pytest.raises(CandidatureInexistante):
            usecase.execute(
                ChangerEtapeCandidaturesCommand(
                    organisme_id=recrutement.organisme_id,
                    recrutement_id=recrutement.offre_id,
                    utilisateur=UtilisateurFactory.create_entity(
                        entity_id=agent_model.utilisateur_id
                    ),
                    etape_cible_id=etape_cible_id,
                    candidatures=unknown_candidature_ids,
                )
            )

    def test_update_batch_isolates_single_failure(
        self,
        recruteur_integration_container,
    ):
        repo = recruteur_integration_container.postgres_candidature_repository()

        models = CandidatureDjangoFactory.create_batch(2)
        candidatures = [repo.mapper.to_domain(m) for m in models]

        unknown_etape_id = uuid4()
        candidatures[1].changer_etape(etape_id=unknown_etape_id)

        result = repo.update_batch(candidatures)

        assert result["successes"][0].entity_id == candidatures[0].entity_id
        assert len(result["failures"]) == 1
        assert result["failures"][0][0] == candidatures[1].entity_id
        assert isinstance(result["failures"][0][1], InfrastructureError)

        models[0].refresh_from_db()
        assert models[0].etape_id == candidatures[0].etape_id
