from datetime import datetime, timezone
from uuid import UUID, uuid4

from faker import Faker
from referentiel.entities.offer import Offer

from application.recruteur.dtos.my_recruits_dtos import (
    CandidaturesCountDTO,
    RecrutementActifDTO,
    RecrutementArchiveDTO,
    ResponsableDTO,
)
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.position_candidature import PositionCandidature
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.mappers.recrutement_mapper import RecrutementMapper
from tests.factories.recruteur.organisme_factory import make_etapes_recrutement

fake = Faker()


class PositionCandidatureFactory:
    @staticmethod
    def create_entity(
        candidature_id: UUID | None = None,
        etape_id: UUID | None = None,
        ordre: int | None = None,
    ) -> PositionCandidature:
        return PositionCandidature(
            candidature_id=candidature_id or uuid4(),
            etape_id=etape_id or uuid4(),
            ordre=ordre,
        )


class RecrutementFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        offre_id: UUID | None = None,
        organisme_id: UUID | None = None,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
        status: RecrutementStatus = RecrutementStatus.ACTIF,
        positions: tuple[PositionCandidature, ...] = (),
        responsables_ids: tuple[UUID, ...] = (),
        derniere_activite_le: datetime | None = None,
        candidat_recrute_id: UUID | None = None,
    ) -> Recrutement:
        return Recrutement.build(
            entity_id=entity_id or uuid4(),
            offre_id=offre_id or uuid4(),
            organisme_id=organisme_id or uuid4(),
            etapes=etapes or make_etapes_recrutement(),
            status=status,
            positions=positions,
            responsables_ids=responsables_ids,
            derniere_activite_le=derniere_activite_le or datetime.now(tz=timezone.utc),
            candidat_recrute_id=candidat_recrute_id,
        )

    @staticmethod
    def create_model(
        offre_id: UUID | None = None,
        organisme_id: UUID | None = None,
        responsables_ids: tuple[UUID, ...] = (),
        status: RecrutementStatus = RecrutementStatus.ACTIF,
        candidat_recrute_id: UUID | None = None,
        **kwargs,
    ) -> RecrutementModel:
        entity = RecrutementFactory.create_entity(
            offre_id=offre_id,
            organisme_id=organisme_id,
            responsables_ids=responsables_ids,
            status=status,
            candidat_recrute_id=candidat_recrute_id,
            **kwargs,
        )
        model = RecrutementMapper().from_domain(entity)
        model.save()
        return model

    @staticmethod
    def create_entity_batch(offers: list[Offer], **kwargs) -> list[Recrutement]:
        return [
            RecrutementFactory.create_entity(offre_id=offer.id, **kwargs)
            for offer in offers
        ]


class RecrutementActifDTOFactory:
    @staticmethod
    def create(
        offer_id: UUID | None = None,
        intitule: str | None = None,
        reference_csp: str | None = None,
        type_contrat: str | None = "TITULAIRE_CONTRACTUEL",
        kind_contrat: str | None = None,
        date_publication: datetime | None = None,
        responsables: list[ResponsableDTO] | None = None,
        derniere_activite: datetime | None = None,
        candidatures: CandidaturesCountDTO | None = None,
    ) -> RecrutementActifDTO:
        return RecrutementActifDTO(
            offer_id=offer_id or uuid4(),
            intitule=intitule or fake.job(),
            reference_csp=reference_csp or fake.bothify(text="REF-###"),
            type_contrat=type_contrat,
            kind_contrat=kind_contrat,
            date_publication=(
                date_publication or fake.date_time_this_year(tzinfo=timezone.utc)
            ),
            responsables=(
                responsables
                if responsables is not None
                else [ResponsableDTO(nom=fake.name())]
            ),
            derniere_activite=(
                derniere_activite or fake.date_time_this_year(tzinfo=timezone.utc)
            ),
            candidatures=candidatures
            or CandidaturesCountDTO(
                total=fake.random_int(min=0, max=20),
                a_traiter=fake.random_int(min=0, max=5),
                en_cours=fake.random_int(min=0, max=10),
            ),
        )


class RecrutementArchiveDTOFactory:
    @staticmethod
    def create(
        offer_id: UUID | None = None,
        intitule: str | None = None,
        reference_csp: str | None = None,
        type_contrat: str | None = None,
        kind_contrat: str | None = None,
        date_publication: datetime | None = None,
        responsables: list[ResponsableDTO] | None = None,
        derniere_activite: datetime | None = None,
        finalise: bool = True,
        recrute: str | None = None,
    ) -> RecrutementArchiveDTO:
        return RecrutementArchiveDTO(
            offer_id=offer_id or uuid4(),
            intitule=intitule or fake.job(),
            reference_csp=reference_csp or fake.bothify(text="REF-###"),
            type_contrat=type_contrat,
            kind_contrat=kind_contrat,
            date_publication=(
                date_publication or fake.date_time_this_year(tzinfo=timezone.utc)
            ),
            responsables=responsables if responsables is not None else [],
            derniere_activite=(
                derniere_activite or fake.date_time_this_year(tzinfo=timezone.utc)
            ),
            finalise=finalise,
            recrute=recrute or fake.name(),
        )
