from application.ingestion.errors.application_errors_ingestion import (
    TalentsoftOrganismeInexistant,
)
from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)


def get_talentsoft_organisme(entity_code: str) -> TalentsoftOrganismeModel:
    try:
        return TalentsoftOrganismeModel.objects.by_entity_code(entity_code).get()
    except TalentsoftOrganismeModel.DoesNotExist as error:
        raise TalentsoftOrganismeInexistant(entity_code) from error
