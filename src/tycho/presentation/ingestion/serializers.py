from datetime import timezone

from rest_framework import serializers

from domain.entities.offer import Offer


class OfferSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    title = serializers.CharField()
    organization = serializers.CharField()
    contract_type = serializers.CharField(allow_null=True)
    category = serializers.CharField(allow_null=True)
    publication_date = serializers.DateTimeField()
    offer_url = serializers.CharField(allow_null=True)

    def to_representation(self, instance: Offer):
        return {
            "external_id": instance.external_id,
            "title": instance.title,
            "organization": instance.organization,
            "contract_type": instance.contract_type.value
            if instance.contract_type
            else None,
            "category": instance.category.value if instance.category else None,
            "publication_date": instance.publication_date.isoformat(),
            "offer_url": str(instance.offer_url) if instance.offer_url else None,
        }


class OfferFiltersSerializer(serializers.Serializer):
    active = serializers.BooleanField(default=True)
    after = serializers.DateTimeField(required=False, default=None)
    before = serializers.DateTimeField(required=False, default=None)

    def validate(self, data):
        after = data.get("after")
        before = data.get("before")
        if after and before and after > before:
            raise serializers.ValidationError("after must be earlier than before.")
        return data

    def validated_datetimes_as_utc(self, data: dict) -> dict:
        for field in ("after", "before"):
            dt = data.get(field)
            if dt and dt.tzinfo is None:
                data[field] = dt.replace(tzinfo=timezone.utc)
        return data
