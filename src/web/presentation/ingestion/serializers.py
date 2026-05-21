from rest_framework import serializers


class ValidationErrorSerializer(serializers.Serializer):
    row = serializers.IntegerField()
    error = serializers.CharField()


class FileErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class NoValidRowsErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
    validation_errors = ValidationErrorSerializer(many=True)


class ServerErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


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


class ListOffersErrorSerializer(serializers.Serializer):
    error = serializers.CharField


class ArchiveOfferRequestSerializer(serializers.Serializer):
    reference = serializers.CharField()
    source_id = serializers.CharField()


class ArchiveOfferSuccessSerializer(serializers.Serializer):
    status = serializers.CharField()
