from rest_framework import serializers


class GenericErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class ValidationErrorSerializer(GenericErrorSerializer):
    row = serializers.IntegerField()


class NoValidRowsErrorSerializer(GenericErrorSerializer):
    validation_errors = ValidationErrorSerializer(many=True)


class TokenErrorMessageSerializer(serializers.Serializer):
    token_class = serializers.CharField()
    token_type = serializers.CharField()
    message = serializers.CharField()


class TokenErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
    messages = TokenErrorMessageSerializer(many=True)


class ConcoursUploadResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    total_rows = serializers.IntegerField()
    valid_rows = serializers.IntegerField()
    invalid_rows = serializers.IntegerField()
    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    validation_errors = ValidationErrorSerializer(many=True, allow_null=True)


class ListOffersResponseSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    title = serializers.CharField()
    organization = serializers.CharField()
    contract_type = serializers.CharField(allow_null=True)
    category = serializers.CharField(allow_null=True)
    publication_date = serializers.DateTimeField()
    offer_url = serializers.CharField(allow_null=True)
    archived_at = serializers.DateTimeField(allow_null=True)


class ListOffersFiltersSerializer(serializers.Serializer):
    active = serializers.BooleanField(default=True)
    external_id_contains = serializers.CharField(default=None)


class ArchiveOfferSuccessSerializer(serializers.Serializer):
    status = serializers.CharField()


class ListMetiersResponseSerializer(serializers.Serializer):
    libelle = serializers.CharField()
    description = serializers.CharField()
    domaine_fonctionnel_code = serializers.CharField()
    versants = serializers.ListField(child=serializers.CharField())
    activites = serializers.ListField(child=serializers.CharField(), allow_null=True)
    conditions_particulieres = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
    offer_family_code = serializers.CharField(allow_null=True)


class ListMetiersFiltersSerializer(serializers.Serializer):
    domain = serializers.CharField(default=None, max_length=3)
