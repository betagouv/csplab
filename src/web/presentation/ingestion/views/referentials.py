from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.country_area import area_for_country
from referentiel.value_objects.departement_region import (
    overseas_region_for_department,
    region_et_zone_pour_departement,
)
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.localisation import FRANCE
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.radius import Radius
from referentiel.value_objects.verse import Verse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from presentation.api.authentication import PublicJwtOnlyMixin
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


def _department_parent_region(code):
    department = Department(code=code)
    # Same rule as offer ingestion: overseas departments belong to DOM or TOM.
    region = overseas_region_for_department(department)
    if region is not None:
        return region.code
    region_et_zone = region_et_zone_pour_departement(department)
    return region_et_zone[0].code if region_et_zone else None


def _department_items():
    items = []
    for code, name in sorted(DEPARTMENT_NAMES.items()):
        parent_code = _department_parent_region(code)
        items.append(
            {
                **_coded_item(code, name),
                "parentCode": parent_code,
                "parentType": "region" if parent_code else "",
            }
        )
    return items


def _region_items():
    regions_with_departments = {
        _department_parent_region(code) for code in DEPARTMENT_NAMES
    }
    return [
        {
            **_coded_item(code, name),
            "parentCode": str(FRANCE),
            "parentType": "country",
            "hasChildren": code in regions_with_departments,
        }
        for code, name in sorted(REGION_NAMES.items())
    ]


def _country_area(code):
    area = area_for_country(Country(code))
    return area.name if area else None


def _country_items():
    items = []
    for code, name in sorted(COUNTRY_NAMES.items()):
        area = _country_area(code)
        items.append(
            {
                **_coded_item(code, name),
                "parentCode": area,
                "parentType": "area" if area else "",
                "hasChildren": code == str(FRANCE),
            }
        )
    return items


def _area_items():
    areas_with_countries = {_country_area(code) for code in COUNTRY_NAMES}
    return [
        {
            **_coded_item(member.name, member.label),
            "hasChildren": member.name in areas_with_countries,
        }
        for member in GeographicalArea
    ]


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
    "area": _area_items,
    "contract_type": lambda: _enum_items(OfferNature),
    "country": _country_items,
    "department": _department_items,
    "domain": lambda: _code_names_items(DOMAIN_NAMES),
    "experience_level": lambda: _enum_items(ExperienceLevel),
    "management": lambda: _enum_items(Management),
    "offer_family_category": lambda: _enum_items(Category),
    "organisation": _organisation_items,
    "radius": lambda: _enum_items(Radius),
    "region": _region_items,
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
        OpenApiParameter(
            name="parentCode",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Ne garde que les valeurs rattachées à ce parent. Pour les lieux, "
                "c'est le `clientCode` du parent : la région pour un département "
                "(ex. `11`, `DOM`, `TOM`), `FRA` pour une région, la zone pour "
                "un pays (ex. `EUROPE`). Pour les "
                "organisations, c'est le `code` de l'organisation parente."
            ),
        ),
    ],
    responses={
        200: FakeTsCodedObjectSerializer(many=True),
        404: GenericErrorSerializer,
    },
)
class ReferentialListView(PublicJwtOnlyMixin, APIView):
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
        parent_code = request.query_params.get("parentCode")
        if parent_code is not None:
            data = [
                item
                for item in data
                if item["parentCode"] is not None
                and str(item["parentCode"]) == parent_code
            ]

        return Response(self.serializer_class(data, many=True).data)
