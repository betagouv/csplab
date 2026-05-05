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
