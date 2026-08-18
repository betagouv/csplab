from uuid import uuid4

from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from pydantic import ValidationError
from referentiel.types import IUpsertResult
from referentiel.value_objects.country import Country
from referentiel.value_objects.departement_region import (
    region_et_zone_pour_departement,
)
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.gateways.finess_gateway_interface import (
    FinessEtablissement,
    IFinessGateway,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.value_objects.siret import SIRET

REFERENTIEL_FINESS = "FINESS"
BATCH_SIZE = 500


def _build_localisation(etablissement: FinessEtablissement) -> Localisation | None:
    if etablissement.departement is None:
        return None

    try:
        department = Department(code=etablissement.departement)
    except ValidationError:
        return None

    region_et_zone = region_et_zone_pour_departement(department)
    if region_et_zone is None:
        return None

    return Localisation(
        area=region_et_zone.area,
        country=Country("FRA"),
        region=region_et_zone.region,
        department=department,
        latitude=etablissement.latitude,
        longitude=etablissement.longitude,
    )


class ImportEtablissementsFinessUsecase(IUseCase[None, IUpsertResult]):
    def __init__(
        self,
        finess_gateway: IFinessGateway,
        organisme_repository: IOrganismeRepository,
        logger: ILogger,
    ):
        self.finess_gateway = finess_gateway
        self.organisme_repository = organisme_repository
        self.logger = logger

    def execute(self, input_data: None = None) -> IUpsertResult:
        resource = self.finess_gateway.find_latest_journalier()
        millesime = resource.millesime.isoformat()
        self.logger.info(
            "Import FINESS: fichier %s (millésime %s)", resource.url, millesime
        )

        result: IUpsertResult = {"created": 0, "updated": 0, "errors": []}
        batch: list[Organisme] = []

        for etablissement in self.finess_gateway.stream_etablissements(resource.url):
            try:
                batch.append(self._to_organisme(etablissement, millesime))
            except Exception as e:  # invalid SIRET, etc.
                result["errors"].append(
                    {
                        "entity_id": etablissement.external_id,
                        "error": str(e),
                        "exception": e,
                    }
                )
                continue

            if len(batch) >= BATCH_SIZE:
                self._flush(batch, result)
                batch = []

        if batch:
            self._flush(batch, result)

        return result

    def _flush(self, batch: list[Organisme], result: IUpsertResult) -> None:
        batch_result = self.organisme_repository.upsert_batch(batch)
        result["created"] += batch_result["created"]
        result["updated"] += batch_result["updated"]
        result["errors"].extend(batch_result["errors"])

    @staticmethod
    def _to_organisme(etablissement: FinessEtablissement, millesime: str) -> Organisme:
        return Organisme.build(
            entity_id=uuid4(),
            nom=etablissement.nom,
            versant=Verse.FPH,
            localisation=_build_localisation(etablissement),
            siret=SIRET(etablissement.siret),
            parent_id=None,
            external_id=etablissement.external_id,
            referentiel=REFERENTIEL_FINESS,
            millesime=millesime,
            gestion_ats=True,
        )
