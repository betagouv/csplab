from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)


class GetRecrutementEtapesUsecase(
    IUsecase[RecrutementRequest, tuple[EtapeRecrutement, ...]]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        recrutement_repository: IRecrutementRepository,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.recrutement_repository = recrutement_repository

    def execute(self, query: RecrutementRequest) -> tuple[EtapeRecrutement, ...]:
        self.organisme_recruteur_repository.get_by_id(query.organisme_id)
        recrutement = self.recrutement_repository.get_by_id(query.recrutement_id)
        if query.organisme_id != recrutement.organisme_id:
            raise OrganismeRecrutementIncoherents(
                query.organisme_id, query.recrutement_id
            )

        # Perf: can_execute() re-checks organisme/recrutement existence already
        # proven by the repository fetches above — dedupe when this usecase
        # migrates to ADR-009.
        can_execute(
            action=OrganismeAction.GET_RECRUTEMENT_ETAPES,
            organisme_id=query.organisme_id,
            recrutement_id=query.recrutement_id,
            utilisateur=query.utilisateur,
        )
        return recrutement.etapes
