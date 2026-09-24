from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.radius import Radius
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from presentation.api.serializers import GenericErrorSerializer
from presentation.ingestion.serializers import (
    COUNTRY_NAMES,
    DEPARTMENT_NAMES,
    DOMAIN_NAMES,
    REGION_NAMES,
    FakeTsCodedObjectSerializer,
)


def _coded_item(client_code, label):
    return {"clientCode": client_code, "label": label}


def _enum_items(enum_cls):
    return [_coded_item(member.name, member.label) for member in enum_cls]


def _code_names_items(names):
    return [_coded_item(code, name) for code, name in sorted(names.items())]


def _organisation_items():
    return [
        {
            "code": organisme.code,
            "clientCode": organisme.entity_code,
            "label": organisme.name,
            "parentCode": organisme.parent_code,
            "parentType": "organisation" if organisme.parent_code else "",
            "hasChildren": organisme.has_children,
        }
        for organisme in TalentsoftOrganismeModel.objects.order_by("entity_code")
    ]


REFERENTIAL_TYPES = {
    "area": lambda: _enum_items(GeographicalArea),
    "contract_type": lambda: _enum_items(ContractType),
    "country": lambda: _code_names_items(COUNTRY_NAMES),
    "department": lambda: _code_names_items(DEPARTMENT_NAMES),
    "domain": lambda: _code_names_items(DOMAIN_NAMES),
    "experience_level": lambda: _enum_items(ExperienceLevel),
    "management": lambda: _enum_items(Management),
    "offer_family_category": lambda: _enum_items(Category),
    "organisation": _organisation_items,
    "radius": lambda: _enum_items(Radius),
    "region": lambda: _code_names_items(REGION_NAMES),
    "verse": lambda: _enum_items(Verse),
    "working_place": lambda: _enum_items(WorkingPlace),
}


@extend_schema(
    summary="Valeurs d'un référentiel (format Talentsoft)",
    description=(
        "Liste les valeurs possibles d'un référentiel utilisé par l'API "
        "fake-ts, au format objet codé Talentsoft."
    ),
    tags=["fake-ts"],
    parameters=[
        OpenApiParameter(
            name="referential_type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            enum=sorted(REFERENTIAL_TYPES),
        ),
    ],
    responses={
        200: FakeTsCodedObjectSerializer(many=True),
        404: GenericErrorSerializer,
    },
)
class ReferentialListView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = FakeTsCodedObjectSerializer

    def get(self, request, referential_type):
        build_items = REFERENTIAL_TYPES.get(referential_type)
        if build_items is None:
            serializer = GenericErrorSerializer(
                {"error": f"Référentiel inconnu : {referential_type}."}
            )
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                "code": None,
                "active": True,
                "parentCode": None,
                "type": referential_type,
                "parentType": "",
                "hasChildren": False,
                **item,
            }
            for item in build_items()
        ]

        return Response(self.serializer_class(data, many=True).data)
