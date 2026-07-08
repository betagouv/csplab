from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.identite.organisme_factory import OrganismeFactory
from tests.factories.recruteur.etapes_recrutement_factory import EtapeRecrutementFactory
from tests.factories.referentiel.offer_factory import OfferFactory


class RecrutementFactory:
    @staticmethod
    def create_entity(
        offre_id: UUID | None = None,
        organisme_id: UUID | None = None,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
        candidatures: tuple[UUID, ...] | None = None,
        responsables: tuple[UUID, ...] | None = None,
        status: StatutRecrutement | None = None,
        candidat_recrute_id: UUID | None = None,
        derniere_activite_le: datetime | None = None,
    ) -> Recrutement:
        return Recrutement.build(
            offre_id=offre_id or uuid4(),
            organisme_id=organisme_id or uuid4(),
            etapes=etapes or EtapeRecrutementFactory.create_entities(),
            candidatures=candidatures or (),
            responsables=responsables or (),
            status=status or StatutRecrutement.ACTIF,
            candidat_recrute_id=candidat_recrute_id,
            derniere_activite_le=derniere_activite_le or datetime.now(tz=timezone.utc),
        )

    @staticmethod
    def create_model(
        offre_id: UUID | None = None,
        organisme_id: UUID | None = None,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
        ordre_etapes: list[str] | None = None,
        responsables_agent_ids: tuple[UUID, ...] | None = None,
    ) -> RecrutementModel:
        if offre_id is None:
            offre_id = OfferFactory.create_model().id
        if organisme_id is None:
            organisme_id = OrganismeFactory.create_model().id
        if etapes is None:
            etapes = EtapeRecrutementFactory.create_entities()

        recrutement = RecrutementModel(
            offre_id=offre_id,
            organisme_id=organisme_id,
            ordre_etapes=ordre_etapes or [str(etape.entity_id) for etape in etapes],
        )
        recrutement.save()

        for etape in etapes:
            model = EtapeModel(
                id=etape.entity_id,
                recrutement=recrutement,
                categorie=etape.categorie.value,
                nom=etape.nom,
                ordre_candidatures=None,
            )
            model.save()

        if responsables_agent_ids is None:
            responsables_agent_ids = (UUID(AgentFactory.create_model().utilisateur_id),)

        for agent_id in responsables_agent_ids:
            RecrutementAgentModel(
                id=uuid4(),
                recrutement=recrutement,
                agent_id=str(agent_id),
            ).save()

        return recrutement
