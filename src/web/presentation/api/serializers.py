from rest_framework import serializers


class GenericErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class TokenErrorMessageSerializer(serializers.Serializer):
    token_class = serializers.CharField()
    token_type = serializers.CharField()
    message = serializers.CharField()


class TokenErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
    messages = TokenErrorMessageSerializer(many=True)
