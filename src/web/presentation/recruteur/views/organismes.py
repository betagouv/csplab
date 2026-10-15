from drf_spectacular.utils import extend_schema, extend_schema_view
from pydantic import ValidationError
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.create_organisme import create_organisme
from application.recruteur.services.list_organismes import list_organismes
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import (
    GenericErrorSerializer,
    generic_response_format,
)
from presentation.recruteur.serializers import (
    CreateOrganismeSerializer,
    OrganismeDetailSerializer,
    OrganismesListSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les organismes",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: OrganismesListSerializer(many=True),
        },
    ),
    post=extend_schema(
        summary="Créer un organisme",
        tags=["recruteur"],
        request=CreateOrganismeSerializer,
        responses={
            **generic_response_format,
            201: OrganismeDetailSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class OrganismesView(SessionApiMixin, APIView):
    serializer_class = OrganismeDetailSerializer

    def get(self, request: Request) -> Response:
        try:
            organismes = list_organismes(utilisateur=request.user)
            return Response(OrganismesListSerializer(organismes, many=True).data)
        except OperationOrganismeRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request: Request) -> Response:
        serializer = CreateOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            organisme = create_organisme(
                nom=serializer.validated_data["nom"],
                versant=Verse(serializer.validated_data["versant"]),
                siret=serializer.validated_data["siret"],
                gestion_ats=serializer.validated_data["gestion_ats"],
                utilisateur=request.user,
            )
            return Response(
                OrganismeDetailSerializer(organisme).data,
                status=status.HTTP_201_CREATED,
            )
        except (OrganismeSiretExisteDeja, ValidationError) as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except OperationOrganismeRefusee as e:
            serializer = GenericErrorSerializer({"error": str(e)})
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
