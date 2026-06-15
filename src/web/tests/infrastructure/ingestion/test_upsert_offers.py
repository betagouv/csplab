from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from faker import Faker
from pydantic import HttpUrl
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.upsert_offers_input import UpsertOffersInput
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from tests.factories.referentiel.offer_factory import OfferFactory

fake = Faker()


def test_upsert_offers_result(ingestion_container):
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
    result = ingestion_container.upsert_offers_usecase().execute(input_data=input_data)

    assert result == {"created": 1, "updated": 1, "errors": []}

    for offer in [existing_offer, new_offer]:
        model = OfferModel.objects.get(external_id=offer.external_id)
        assert OfferModel.to_entity(model) == offer
