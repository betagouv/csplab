from datetime import datetime

import polars as pl
from asgiref.sync import async_to_sync
from drf_spectacular.utils import (
    PolymorphicProxySerializer,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from pydantic import ValidationError
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from domain.exceptions.offer_errors import OfferDoesNotExist
from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
    UserRateThrottleExceptApiKey,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.openapi import (
    CONCOURS_UPLOAD_DESCRIPTION,
    CONCOURS_UPLOAD_EXAMPLES,
    LIST_OFFERS_DESCRIPTION,
    LIST_OFFERS_EXAMPLES,
)
from presentation.ingestion.pagination import IngestionPagination
from presentation.ingestion.schemas import ConcoursRowSchema
from presentation.ingestion.serializers import (
    ArchiveOfferSuccessSerializer,
    ConcoursUploadResponseSerializer,
    FileErrorSerializer,
    ListOffersErrorSerializer,
    ListOffersFiltersSerializer,
    ListOffersResponseSerializer,
    NoValidRowsErrorSerializer,
    ServerErrorSerializer,
    TokenErrorSerializer,
)

# Mapping from CSV column names to Python field names
CSV_TO_PYTHON_MAPPING = {
    "N° NOR": "nor",
    "N° NOR de référence": "nor_reference",
    "Ministère": "ministere",
    "Ministère (saisie initiale)": "ministere_initial",
    "Catégorie": "categorie",
    "Corps": "corps",
    "Grade": "grade",
    "Corps/Grade (saisie initiale)": "corps_grade_initial",
    "Direction/Établissement": "direction_etablissement",
    "Année de référence": "annee_reference",
    "Statut": "statut",
    "Date de première épreuve": "date_premiere_epreuve",
    "National": "national",
    "National à affectation locale": "national_affectation_locale",
    "Déconcentré": "deconcentre",
    "Externe": "externe",
    "Interne": "interne",
    "Troisieme Concours": "troisieme_concours",
    "Unique": "unique",
    "Examen professionnel": "examen_professionnel",
    "Sans concours externe": "sans_concours_externe",
    "Pacte": "pacte",
    "Sélection professionnelle": "selection_professionnelle",
    "Concours spécial": "concours_special",
    "Concours réservé": "concours_reserve",
    "Sans concours interne réservé": "sans_concours_interne_reserve",
    "Examen professionnalisé réservé": "examen_professionnalise_reserve",
    "Interne exceptionnel": "interne_exceptionnel",
    "Apprenti BOETH": "apprenti_boeth",
    "Promotion BOETH": "promotion_boeth",
    "Autres": "autres",
    "Nb postes ACVG": "nb_postes_acvg",
    "Nb postes TH": "nb_postes_th",
    "Nb postes total": "nb_postes_total",
}


def map_csv_to_python_columns(csv_data):
    mapped_data = {}
    for csv_name, value in csv_data.items():
        python_name = CSV_TO_PYTHON_MAPPING.get(csv_name, csv_name)
        mapped_data[python_name] = value
    return mapped_data


def format_validation_error(error: ValidationError) -> str:
    errors = []
    for err in error.errors():
        field = err["loc"][0] if err["loc"] else "unknown"
        msg = err["msg"]

        # Simplify common error messages
        if "Input should be a valid string" in msg and err.get("input") is None:
            errors.append(f"Le champ '{field}' est requis")
        elif "Input should be greater than or equal to" in msg:
            ge_value = err.get("ctx", {}).get("ge", "")
            errors.append(f"Le champ '{field}' doit être >= {ge_value}")
        elif "Input should be a valid boolean" in msg:
            errors.append(f"Le champ '{field}' doit être Oui/Non")
        elif "Date must be in DD/MM/YYYY format" in msg:
            errors.append(f"Le champ '{field}' doit être au format JJ/MM/AAAA")
        else:
            errors.append(f"Erreur dans '{field}': {msg}")

    return " | ".join(errors)


class ConcoursUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Upload et traitement d'un fichier CSV de concours GRECO",
        description=CONCOURS_UPLOAD_DESCRIPTION,
        examples=CONCOURS_UPLOAD_EXAMPLES,
        tags=["concours"],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Fichier CSV contenant les données de concours",
                    }
                },
                "required": ["file"],
            }
        },
        responses={
            201: ConcoursUploadResponseSerializer,
            400: PolymorphicProxySerializer(
                component_name="ConcoursUpload400Error",
                serializers=[FileErrorSerializer, NoValidRowsErrorSerializer],
                resource_type_field_name=None,
            ),
            401: TokenErrorSerializer,
            500: ServerErrorSerializer,
        },
    )
    def post(self, request):
        container = create_ingestion_container()
        logger = container.logger_service()

        # Validate file presence and type
        file_validation_response = self._validate_file(request, logger)
        if file_validation_response:
            return file_validation_response

        csv_file = request.FILES["file"]
        logger.info("Processing CSV file: %s (%d bytes)", csv_file.name, csv_file.size)

        try:
            df = pl.read_csv(csv_file, separator=";")
            rows = df.to_dicts()
            logger.info("CSV parsed successfully: %d rows found", len(rows))

            # Process and validate rows
            valid_documents, validation_errors = self._process_csv_rows(rows, logger)

            if not valid_documents:
                return self._handle_no_valid_documents(validation_errors)

            # Execute usecase
            result = self._execute_load_documents_usecase(
                container, valid_documents, logger
            )

            return self._create_success_response(
                rows, valid_documents, validation_errors, result, logger
            )

        except pl.exceptions.ComputeError as e:
            logger.error("CSV parsing error: %s", str(e))
            return Response(
                {"error": "CSV parsing error"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error("Unexpected error during CSV upload: %s", str(e))
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _validate_file(self, request, logger):
        file_name = (
            request.FILES.get("file", {}).name if "file" in request.FILES else "no file"
        )
        logger.info("CSV upload request received: %s", file_name)

        if "file" not in request.FILES:
            logger.warning("No file provided in upload request")
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES["file"]
        if not csv_file.name.endswith(".csv"):
            logger.warning("Invalid file type: %s", csv_file.name)
            return Response(
                {"error": "File must be a CSV"}, status=status.HTTP_400_BAD_REQUEST
            )

        return None

    def _process_csv_rows(self, rows, logger):
        valid_documents = []
        validation_errors = []
        current_time = datetime.now()

        for index, row_dict in enumerate(rows):
            try:
                document = self._process_single_row(row_dict, current_time)
                if document:
                    valid_documents.append(document)
                else:
                    validation_errors.append(
                        {"row": index + 1, "error": "N° NOR manquant"}
                    )

            except ValidationError as e:
                validation_errors.append(
                    {"row": index + 1, "error": format_validation_error(e)}
                )
            except Exception:
                validation_errors.append(
                    {
                        "row": index + 1,
                        "error": f"Error processing on line {index + 1}",
                    }
                )

        logger.info(
            f"Validation completed: {len(valid_documents)} valid, "
            f"{len(validation_errors)} errors"
        )

        return valid_documents, validation_errors

    def _process_single_row(self, row_dict, current_time):
        # Map CSV column names to Python field names
        mapped_row = map_csv_to_python_columns(row_dict)

        # Clean the data: convert None, empty strings, and "null" to None
        cleaned_row = {}
        for k, v in mapped_row.items():
            if v is None or v == "" or str(v).lower() == "null":
                cleaned_row[k] = None
            else:
                cleaned_row[k] = v

        validated_row = ConcoursRowSchema(**cleaned_row)
        raw_data = validated_row.model_dump()

        # Use nor as external_id for CONCOURS
        nor_value = validated_row.nor
        if not nor_value:
            return None

        return Document(
            external_id=nor_value,
            raw_data=raw_data,
            type=DocumentType.CONCOURS,
            created_at=current_time,
        )

    def _handle_no_valid_documents(self, validation_errors):
        return Response(
            {
                "error": "No valid rows found",
                "validation_errors": validation_errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _execute_load_documents_usecase(self, container, valid_documents, logger):
        logger.info(
            f"Executing load documents usecase with {len(valid_documents)} documents"
        )
        usecase = container.load_documents_usecase()
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.UPLOAD_FROM_CSV,
            kwargs={
                "documents": valid_documents,
                "document_type": DocumentType.CONCOURS,
            },
        )
        return async_to_sync(usecase.execute)(input_data)

    def _create_success_response(
        self, rows, valid_documents, validation_errors, result, logger
    ):
        created = result.get("created", 0)
        updated = result.get("updated", 0)
        logger.info(
            f"Upload completed successfully: created={created}, updated={updated}"
        )

        return Response(
            {
                "status": "success",
                "message": (
                    f"Successfully processed {len(valid_documents)} "
                    "valid concours records"
                ),
                "total_rows": len(rows),
                "valid_rows": len(valid_documents),
                "invalid_rows": len(validation_errors),
                "created": result.get("created", 0),
                "updated": result.get("updated", 0),
                "validation_errors": validation_errors if validation_errors else None,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    summary="Liste des offres",
    description=LIST_OFFERS_DESCRIPTION,
    examples=LIST_OFFERS_EXAMPLES,
    tags=["offres"],
    responses={
        200: ListOffersResponseSerializer,
        400: ListOffersErrorSerializer,
        401: TokenErrorSerializer,
        500: ServerErrorSerializer,
    },
)
class OffersListView(APIView):
    serializer_class = ListOffersResponseSerializer
    usecase = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_ingestion_container()
        self.logger = self.container.logger_service()
        if self.usecase is None:
            self.usecase = self.container.list_offers_usecase()

    def get(self, request):
        try:
            filters = ListOffersFiltersSerializer(data=self.request.query_params)
            filters.is_valid(raise_exception=True)
            input_data = GetFilteredOffersInput(**filters.validated_data)

            result = self.usecase.execute(input_data)

            paginator = IngestionPagination()
            items = paginator.paginate(result.page, request)
            return paginator.get_paginated_response(
                ListOffersResponseSerializer(items, many=True).data
            )
        except Exception as e:
            self.logger.error("Unexpected error in OffersListView: %s", str(e))
            serializer = ServerErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    post=extend_schema(
        request=None,
        summary="Archiver une offre par référence",
        description=(
            "Archive une offre selon sa référence. "
            "Accepte une authentification JWT ou par clé d'API."
        ),
        tags=["offres"],
        responses={
            200: ArchiveOfferSuccessSerializer,
            401: PolymorphicProxySerializer(
                component_name="ArchiveOffer401Error",
                serializers=[
                    TokenErrorSerializer,
                    inline_serializer(
                        name="ArchiveOfferUnauthorized",
                        fields={"detail": drf_serializers.CharField()},
                    ),
                ],
                resource_type_field_name=None,
            ),
            404: inline_serializer(
                name="ArchiveOfferNotFound",
                fields={"detail": drf_serializers.CharField()},
            ),
        },
    )
)
class ArchiveOffersView(APIView):
    authentication_classes = [JWTAuthentication, ApiKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottleExceptApiKey]

    serializer_class = ArchiveOfferSuccessSerializer

    def post(self, request, reference: str):
        container = create_ingestion_container()
        use_case = container.archive_offer_by_reference_usecase()
        try:
            use_case.execute(reference)
        except OfferDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
