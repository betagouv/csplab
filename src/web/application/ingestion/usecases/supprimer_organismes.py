from application.ingestion.interfaces.supprimer_organismes_input import (
    SupprimerOrganismesInput,
)
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)


class SupprimerOrganismesUsecase:
    def __init__(
        self,
        organisme_repository: PostgresOrganismeRepository,
    ):
        self.organisme_repository = organisme_repository

    def execute(self, input_data: SupprimerOrganismesInput):
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
            found_organismes.append(organisme)

        deleted = self.organisme_repository.supprimer_batch(found_organismes)
        return {"deleted": deleted, "not_found": not_found}
