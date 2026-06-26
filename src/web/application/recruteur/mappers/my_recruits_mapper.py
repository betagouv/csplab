from uuid import UUID

from ddd.mapper_interface import IFromDomainMapper
from referentiel.entities.offer import Offer

from application.recruteur.dtos.my_recruits_dtos import (
    CandidaturesCountDTO,
    RecrutementActifDTO,
    RecrutementArchiveDTO,
    RecrutementDTO,
    RecrutementItem,
    ResponsableDTO,
)
from domain.identite.entities.agent import Agent
from domain.identite.entities.candidat import Candidat
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus


class RecrutementMapper(IFromDomainMapper[Recrutement, RecrutementItem]):
    def __init__(
        self,
        offers: dict[UUID, Offer],
        agents: dict[UUID, Agent],
        candidats: dict[UUID, Candidat],
        status: RecrutementStatus,
    ) -> None:
        self._offers = offers
        self._agents = agents
        self._candidats = candidats
        self._status = status

    def from_domain(
        self, recrutement: Recrutement
    ) -> RecrutementActifDTO | RecrutementArchiveDTO:
        offer = self._offers[recrutement.offre_id]

        responsables = [
            ResponsableDTO(
                nom=f"{a.prenom} {a.nom}" if (a := self._agents.get(uid)) else str(uid)
            )
            for uid in recrutement.responsables_ids
        ]

        base = RecrutementDTO(
            offer_id=offer.id,
            intitule=offer.title,
            reference_csp=offer.reference,
            type_contrat=(offer.contract_type.value if offer.contract_type else None),
            type_offre=None,
            date_publication=offer.publication_date,
            responsables=responsables,
            derniere_activite=recrutement.derniere_activite_le,
        )

        if self._status == RecrutementStatus.ACTIF:
            entree_id = next(
                (
                    e.entity_id
                    for e in recrutement.etapes
                    if e.categorie == CategorieEtapeRecrutement.ENTREE
                ),
                None,
            )
            en_cours_ids = {
                e.entity_id
                for e in recrutement.etapes
                if e.categorie == CategorieEtapeRecrutement.EN_COURS
            }
            return RecrutementActifDTO(
                **vars(base),
                candidatures=CandidaturesCountDTO(
                    total=len(recrutement.positions),
                    a_traiter=sum(
                        1 for p in recrutement.positions if p.etape_id == entree_id
                    ),
                    en_cours=sum(
                        1 for p in recrutement.positions if p.etape_id in en_cours_ids
                    ),
                ),
            )

        # ARCHIVE
        recrute_nom: str | None = None
        if recrutement.candidat_recrute_id:
            candidat = self._candidats.get(recrutement.candidat_recrute_id)
            if candidat:
                recrute_nom = f"{candidat.prenom} {candidat.nom}"

        return RecrutementArchiveDTO(
            **vars(base),
            finalise=True if recrutement.candidat_recrute_id else False,
            recrute=recrute_nom,
        )
