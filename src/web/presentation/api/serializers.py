from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from presentation.api.changelog_api import TYPE_LABELS, Fragment, TypeChangement


class GenericErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class DetailErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class TokenErrorMessageSerializer(serializers.Serializer):
    token_class = serializers.CharField()
    token_type = serializers.CharField()
    message = serializers.CharField()


class TokenErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
    messages = TokenErrorMessageSerializer(many=True)


generic_response_format = {
    401: TokenErrorSerializer,
    403: GenericErrorSerializer,
    404: GenericErrorSerializer,
    500: GenericErrorSerializer,
}


class ChangelogSubsectionSerializer(serializers.Serializer):
    titre = serializers.CharField()
    contenu = serializers.CharField()


class ChangelogEntrySerializer(serializers.Serializer):
    id = serializers.CharField(source="slug")
    date = serializers.DateField()
    type = serializers.ChoiceField(choices=TypeChangement.choices)
    libelle_type = serializers.SerializerMethodField()
    routes = serializers.ListField(child=serializers.CharField())
    pr = serializers.IntegerField()
    pr_url = serializers.URLField()
    liens = serializers.ListField(child=serializers.URLField())
    url = serializers.SerializerMethodField()
    contenu = serializers.CharField(source="entry")
    sous_sections = serializers.SerializerMethodField()

    def get_libelle_type(self, fragment: Fragment) -> str:
        return TYPE_LABELS[fragment.type]

    def get_url(self, fragment: Fragment) -> str:
        return f"{self.context['page_url']}#{fragment.slug}"

    @extend_schema_field(ChangelogSubsectionSerializer(many=True))
    def get_sous_sections(self, fragment: Fragment) -> list[dict[str, str]]:
        return [
            {"titre": title, "contenu": text} for title, text in fragment.subsections
        ]


class ChangelogSerializer(serializers.Serializer):
    nombre = serializers.IntegerField()
    entrees = ChangelogEntrySerializer(many=True)


class ChangelogErrorSerializer(serializers.Serializer):
    erreurs = serializers.ListField(child=serializers.CharField())
