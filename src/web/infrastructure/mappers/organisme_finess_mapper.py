from uuid import uuid4

from ddd.mapper_interface import IToDomainMapper
from pydantic import ValidationError
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.errors.organisme_errors import EtablissementInvalideError
from domain.identite.value_objects.siret import SIRET
from infrastructure.external_gateways.dtos.finess_dtos import EtablissementDTO

REFERENTIEL_FINESS = "FINESS"


class OrganismeFinessMapper(IToDomainMapper[EtablissementDTO, Organisme]):
    def to_domain(self, dto: EtablissementDTO) -> Organisme:
        try:
            return Organisme.build(
                entity_id=uuid4(),
                nom=dto.nom,
                versant=Verse.FPH,
                localisation=self._build_localisation(dto),
                siret=SIRET(dto.siret),
                parent_id=None,
                external_id=dto.external_id,
                referentiel=REFERENTIEL_FINESS,
                millesime=dto.millesime,
                gestion_ats=False,
            )
        except Exception as err:  # invalid SIRET, etc.
            raise EtablissementInvalideError(dto.external_id, err) from err

    @staticmethod
    def _build_localisation(dto: EtablissementDTO) -> Localisation | None:
        if dto.departement is None:
            return None

        try:
            department = Department(code=dto.departement)
        except ValidationError:
            return None

        return Localisation.from_department(
            department,
            latitude=dto.latitude,
            longitude=dto.longitude,
        )
