from presentation.ingestion.serializers import OffersInputSerializer
from tests.factories.ingestion.offer_payload_factory import PayloadOfferFactory


def test_offers_input_serializer_never_exposes_archived_at():
    assert "archived_at" not in OffersInputSerializer().fields

    payload = PayloadOfferFactory.create(
        identification={"reference": "REF-001", "versant": "FPT"},
        archived_at="2024-01-01T00:00:00Z",
    )
    serializer = OffersInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    assert "archived_at" not in serializer.validated_data
