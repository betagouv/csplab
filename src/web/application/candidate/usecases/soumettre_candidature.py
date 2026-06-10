from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase

from application.candidate.commands.soumettre_candidature_command import (
    SoumettreCandidatureCommand,
)
from domain.candidate.entities.candidature import Candidature
from domain.candidate.events.candidature_events import DossierCandidatureInitialise
from domain.candidate.exceptions.candidature_errors import CandidatureNexistePas
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)


class SoumettreCandidatureUsecase(
    IUseCase[SoumettreCandidatureCommand, Candidature],
):
    def __init__(
        self,
        candidature_repository: ICandidatureRepository,
        logger: ILogger,
    ):
        self.logger = logger
        self.candidature_repository = candidature_repository

    def execute(self, command: SoumettreCandidatureCommand) -> Candidature:
        self.logger.info(
            "Starting candidature submission for candidate_uuid='%s', offer_uuid=%d",
        )
        offre_id = command.offre_id
        candidat_id = command.candidat_id
        # todo: rbac should manage access:
        # candidate can only get access to its candidatures
        candidature = None
        try:
            props = self.candidature_repository.get_by_offer(offre_id, candidat_id)
            candidature = Candidature.build(
                props.candidat_id,
                props.offre_id,
                props.statut,
                props.documents,
                props.soumise_le,
                props.mise_a_jour_le,
            )
        except CandidatureNexistePas as e:
            self.logger.info(e.message)
            candidature = Candidature.create(
                DossierCandidatureInitialise(offre_id, candidat_id)
            )

        self.candidature_repository.save(candidature)
        return candidature
        # todo entity document.
