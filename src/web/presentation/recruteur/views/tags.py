from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from application.recruteur.services.create_tag import create_tag
from application.recruteur.services.list_tags import list_tags
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.tag_errors import InvalidTagName, TagAlreadyExists
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import (
    CreateTagSerializer,
    TagListQuerySerializer,
    TagSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Liste des étiquettes d'un organisme",
        tags=["recruteur"],
        parameters=[TagListQuerySerializer],
        responses={
            **generic_response_format,
            200: TagSerializer(many=True),
            400: GenericErrorSerializer,
        },
    ),
    post=extend_schema(
        summary="Créer une étiquette dans un organisme",
        tags=["recruteur"],
        request=CreateTagSerializer,
        responses={
            **generic_response_format,
            201: TagSerializer,
            400: GenericErrorSerializer,
            409: GenericErrorSerializer,
        },
    ),
)
class OrganismeTagsView(SessionApiMixin, ListAPIView):
    serializer_class = TagSerializer

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (AccesOrganismeRefuse, OperationOrganismeRefusee, AccesRecrutementInconnu),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(exc, OrganismeNexistePas):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, InvalidTagName):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if isinstance(exc, TagAlreadyExists):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_409_CONFLICT,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def get_queryset(self):
        query = TagListQuerySerializer(data=self.request.query_params)
        query.is_valid(raise_exception=True)
        return list_tags(
            organisme_id=self.kwargs["organisme_uuid"],
            utilisateur=self.request.user,
            category=query.validated_data.get("category"),
        )

    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = CreateTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tag = create_tag(
            organisme_id=organisme_uuid,
            utilisateur=request.user,
            name=serializer.validated_data["name"],
            category=serializer.validated_data["category"],
            color=serializer.validated_data["color"],
        )
        return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
