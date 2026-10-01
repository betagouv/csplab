from datetime import datetime, timezone
from time import time

import pytest
from faker import Faker

from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    CachedToken,
    TalentsoftDetailOffer,
    TalentsoftOrganisationPayload,
)
from tests.factories.talentsoft_factories import (
    TalentsoftCodedObjectFactory,
    TalentsoftDetailOfferFactory,
    TalentsoftOfferFactory,
    TalentsoftOrganisationFactory,
)

fake = Faker()


@pytest.mark.parametrize(
    "delay,is_valid", [(100, True), (31, True), (30, False), (-100, False)]
)
def test_is_valid_cached_token(delay, is_valid):
    token = CachedToken(
        access_token=fake.uuid4(),
        token_type=fake.word().capitalize(),
        expires_at_epoch=time() + delay,
    )

    assert token.is_valid() == is_valid


def test_modification_date_defaults_to_now_when_null():
    before = datetime.now(timezone.utc)

    offer = TalentsoftOfferFactory.build(modificationDate=None)

    assert offer.modificationDate is not None
    modification_date = datetime.fromisoformat(
        offer.modificationDate.replace("Z", "+00:00")
    )
    after = datetime.now(timezone.utc)
    assert before <= modification_date <= after


def test_organisation_payload_merges_referentiel_and_detail():
    referentiel = TalentsoftCodedObjectFactory.build(
        code=12903, parentCode=12899, hasChildren=True
    )
    detail = TalentsoftOrganisationFactory.build()

    payload = TalentsoftOrganisationPayload.from_referentiel_and_detail(
        referentiel, detail
    )

    assert payload.code == 12903
    assert payload.parentCode == 12899
    assert payload.hasChildren is True
    assert payload.entityCode == detail.entityCode
    assert payload.name == detail.name


def test_organisation_payload_defaults_when_no_parent():
    referentiel = TalentsoftCodedObjectFactory.build(
        code=1, parentCode=None, hasChildren=False
    )
    detail = TalentsoftOrganisationFactory.build()

    payload = TalentsoftOrganisationPayload.from_referentiel_and_detail(
        referentiel, detail
    )

    assert payload.parentCode is None
    assert payload.hasChildren is False


def _referential_item(client_code: str) -> dict:
    return {
        "code": 1,
        "clientCode": client_code,
        "label": client_code,
        "active": True,
        "type": "type",
        "_links": [{"href": "https://example.com", "rel": "self"}],
    }


def test_detail_offer_parses_spec_fields():
    data = TalentsoftDetailOfferFactory.build().model_dump(by_alias=True)
    data |= {
        "applicationQuestions": [
            {
                "question": _referential_item("Q1"),
                "answers": [_referential_item("A1"), _referential_item("A2")],
                "isRequired": True,
            }
        ],
        "operationalManager": {"language": _referential_item("fr-FR")},
        "mainSupervisor": {"firstName": "Camille", "lastName": "Martin"},
        "numberOfVacancies": 2,
        "profileCollection": [_referential_item("P1")],
        "locations": [{"displayedAddress": "Paris", "position": {"lat": 1, "lon": 2}}],
        "_format": {"title": "Titre"},
        "_metadata": {"blocks": [{"blockIdentifier": "offer"}]},
        "_applicationformmetadata": {"blocks": [{"fields": [{"name": "email"}]}]},
        "customFields": {
            "description": {"shortText1": "CDI"},
            "offerCustomBlock2": {"longText1": "Texte"},
        },
    }

    offer = TalentsoftDetailOffer.model_validate(data)

    assert offer.applicationQuestions[0].question is not None
    assert offer.applicationQuestions[0].question.clientCode == "Q1"
    assert [a.clientCode for a in offer.applicationQuestions[0].answers] == ["A1", "A2"]
    assert offer.operationalManager is not None
    assert offer.operationalManager.language is not None
    assert offer.operationalManager.language.clientCode == "fr-FR"
    assert offer.mainSupervisor is not None
    assert offer.mainSupervisor.lastName == "Martin"
    assert offer.numberOfVacancies == 2
    assert offer.profileCollection[0].links[0].rel == "self"
    assert offer.locations[0].displayedAddress == "Paris"
    assert offer.format is not None and offer.format.title == "Titre"
    assert offer.metadata is not None
    assert offer.metadata.blocks[0].blockIdentifier == "offer"
    assert offer.applicationFormMetadata is not None
    assert offer.applicationFormMetadata.blocks[0].fields[0].name == "email"
    assert offer.customFields is not None
    assert offer.customFields.description is not None
    assert offer.customFields.description.shortText1 == "CDI"
    assert offer.customFields.offerCustomBlock2 is not None
    assert offer.customFields.offerCustomBlock2.longText1 == "Texte"
