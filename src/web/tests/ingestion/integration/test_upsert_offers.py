from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from faker import Faker
from pydantic import HttpUrl

from application.ingestion.interfaces.upsert_offers_input import (
    UpsertOffersInput,
)
from config.app_config import AppConfig
from domain.value_objects.area import GeographicalArea
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.offer_factory import OfferFactory

fake = Faker()


@pytest.fixture(name="documents_integration_container")
def documents_integration_container_fixture(db):
    container = IngestionContainer()
    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    return container


def test_upsert_offers_result(documents_integration_container):
    offer = OfferFactory.create_model(
        verse=Verse.FPE,
        category=Category.B,
        contract_type=ContractType.CONTRACTUELS,
        localisation=Localisation(
            area=GeographicalArea("AS"),
            country=Country("GUF"),
            region=Region(code="03"),
            department=Department(code="973"),
        ),
    )
    existing_offer = OfferModel.to_entity(offer)
    updated_fields = {
        "verse": Verse.FPT,
        "title": fake.word(),
        "profile": fake.sentence(),
        "mission": fake.sentence(),
        "category": Category.C,
        "contract_type": ContractType.TITULAIRE_CONTRACTUEL,
        "organization": fake.name(),
        "offer_url": HttpUrl(f"https://fake.url/offer/{existing_offer.external_id}"),
        "code_emploi_csp": fake.word(),
        "localisation": Localisation(
            area=GeographicalArea("AF"),
            country=Country("FRA"),
            region=Region(code="04"),
            department=Department(code="76"),
        ),
        "publication_date": datetime.now(timezone.utc) - relativedelta(days=1),
        "beginning_date": LimitDate(datetime.now(timezone.utc) + relativedelta(days=1)),
    }
    for field, value in updated_fields.items():
        setattr(existing_offer, field, value)

    new_offer = OfferFactory.create_entity(source_id=existing_offer.source_id)

    input_data = UpsertOffersInput(offers=[existing_offer, new_offer])
    result = documents_integration_container.upsert_offers_usecase().execute(
        input_data=input_data
    )

    assert result == {"created": 1, "updated": 1, "errors": []}

    for offer in [existing_offer, new_offer]:
        model = OfferModel.objects.get(external_id=offer.external_id)
        assert OfferModel.to_entity(model) == offer
