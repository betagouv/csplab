from uuid import UUID, uuid4

from faker import Faker
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.mappers.organisme_identite_mapper import (
    OrganismeIdentiteMapper,
)
from infrastructure.mappers.organisme_recruteur_mapper import (
    OrganismeRecruteurMapper,
)


def make_localisation(
    department: str = "75",
    region: str = "11",
    country: str = "FRA",
) -> Localisation:
    return Localisation(
        area=GeographicalArea.EUROPE,
        country=Country(country),
        region=Region(code=region),
        department=Department(code=department),
    )


_fake = Faker("fr_FR")


class OrganismeFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        nom: str = "Ministère de l'Économie, des Finances et de la Relance",
        versant: Verse = Verse.FPE,
        localisation: Localisation | None = None,
        siret: SIRET | None = None,
    ) -> Organisme:
        return Organisme.build(
            entity_id=entity_id or uuid4(),
            nom=nom,
            versant=versant,
            localisation=localisation or make_localisation(),
            siret=siret or SIRET(_fake.siret().replace(" ", "")),
        )

    @staticmethod
    def create_model(
        entity_id: UUID | None = None,
        nom: str = "Ministère de l'Économie, des Finances et de la Relance",
        versant: Verse = Verse.FPE,
        localisation: Localisation | None = None,
        siret: SIRET | None = None,
        etapes: tuple[EtapeRecrutement, ...] | None = None,
        agent_id: UUID | None = None,
        role: AgentOrganismeRole | None = None,
    ):
        organisme = OrganismeFactory.create_entity(
            entity_id=entity_id,
            nom=nom,
            versant=versant,
            localisation=localisation,
            siret=siret or SIRET(_fake.siret().replace(" ", "")),
        )
        mapper = OrganismeIdentiteMapper()
        model = mapper.from_domain(organisme)
        if etapes is not None:
            model.etapes = OrganismeRecruteurMapper().from_domain(etapes)
        model.save()
        if agent_id is not None:
            OrganismeAgentModel(
                id=uuid4(),
                organisme_id=model.id,
                agent_id=agent_id,
                role=(role or AgentOrganismeRole.MEMBRE).value,
            ).save()
        return model
