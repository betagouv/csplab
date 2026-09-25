from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.mappers import TalentsoftOrganisationOutputMapper
from presentation.ingestion.serializers import FakeTsOrganisationSerializer


@extend_schema(
    summary="Détail d'une organisation (format Talentsoft)",
    description="Simule l'API Talentsoft `organisation/{id}`, à partir de "
    "l'`entityCode` de l'organisation.",
    tags=["fake-ts"],
    responses={
        200: FakeTsOrganisationSerializer,
        404: GenericErrorSerializer,
    },
)
class OrganisationDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = FakeTsOrganisationSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapper = TalentsoftOrganisationOutputMapper()

    def get(self, request, entity_code):
        organisme = TalentsoftOrganismeModel.objects.by_entity_code(entity_code).first()
        if organisme is None:
            serializer = GenericErrorSerializer(
                {"error": f"Organisation inconnue : {entity_code}."}
            )
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(
            self.serializer_class(self.mapper.to_dict(organisme.to_entity())).data
        )
