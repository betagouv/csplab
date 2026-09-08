from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUsecase
from referentiel.types import IDeleteResult

from application.ingestion.interfaces.supprimer_organismes_input import (
    SupprimerOrganismesInput,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)


class SupprimerOrganismesUsecase(IUsecase[SupprimerOrganismesInput, IDeleteResult]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        logger: ILogger,
    ):
        self.organisme_repository = organisme_repository
        self.logger = logger

    def execute(self, input_data: SupprimerOrganismesInput) -> IDeleteResult:
        pairs = [(data.referentiel, data.external_id) for data in input_data.organismes]
        organismes_by_pair = (
            self.organisme_repository.get_by_referentiel_and_external_id_batch(pairs)
        )

        found_organismes = []
        not_found = []
        for referentiel, external_id in pairs:
            organisme = organismes_by_pair.get((referentiel, external_id))
            if organisme is None:
                not_found.append(
                    {"referentiel": referentiel, "external_id": external_id}
                )
                continue
            organisme.supprimer()
            found_organismes.append(organisme)

        deleted = self.organisme_repository.supprimer_batch(found_organismes)
        self.logger.info(
            "SupprimerOrganismes: deleted=%d not_found=%d",
            deleted,
            len(not_found),
        )
        return {"deleted": deleted, "not_found": not_found}
