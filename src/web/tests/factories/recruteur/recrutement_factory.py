from datetime import datetime, timezone
from uuid import UUID, uuid4

from application.recruteur.dtos.recrutement_read_models import (
    CandidaturesCompteurDto,
    RecrutementActifsReadModel,
    RecrutementArchivesReadModel,
    ResponsableDto,
)
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
    def create_actif_read_model(
        offer_id: UUID | None = None,
        intitule: str | None = None,
        reference_csp: str | None = None,
        type_contrat: str | None = None,
        date_publication: datetime | None = None,
        responsables: list[ResponsableDto] | None = None,
        derniere_activite: datetime | None = None,
        candidatures: CandidaturesCompteurDto | None = None,
    ) -> RecrutementActifsReadModel:
        return RecrutementActifsReadModel(
            offer_id=offer_id or uuid4(),
            intitule=intitule or "",
            reference_csp=reference_csp or "",
            type_contrat=type_contrat or "TITULAIRE_CONTRACTUEL",
            date_publication=date_publication or datetime.now(tz=timezone.utc),
            responsables=responsables or [ResponsableDto(nom="Dupont")],
            derniere_activite=derniere_activite or datetime.now(tz=timezone.utc),
            candidatures=candidatures
            or CandidaturesCompteurDto(total=0, a_traiter=0, en_cours=0),
        )

    @staticmethod
    def create_archive_read_model(
        offer_id: UUID | None = None,
        intitule: str | None = None,
        reference_csp: str | None = None,
        type_contrat: str | None = None,
        date_archivage: datetime | None = None,
        responsables: list[ResponsableDto] | None = None,
        finalise: bool = False,
        recrute: str | None = None,
    ) -> RecrutementArchivesReadModel:
        return RecrutementArchivesReadModel(
            offer_id=offer_id or uuid4(),
            intitule=intitule or "",
            reference_csp=reference_csp or "",
            type_contrat=type_contrat or "TITULAIRE_CONTRACTUEL",
            date_archivage=date_archivage or datetime.now(tz=timezone.utc),
            responsables=responsables or [ResponsableDto(nom="Dupont")],
            finalise=finalise,
            recrute=recrute,
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
