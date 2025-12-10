"""Views for ingestion API endpoints."""

from datetime import datetime

import polars as pl
from pydantic import ValidationError
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.application.interfaces.load_documents_input import (
    LoadDocumentsInput,
)
from apps.ingestion.application.interfaces.load_operation_type import LoadOperationType
from apps.ingestion.container_singleton import IngestionContainerSingleton
from core.entities.document import Document, DocumentType
from core.errors.document_error import InvalidDocumentTypeError

from .schemas import ConcoursRowSchema


def format_validation_error(error: ValidationError) -> str:
    """Format Pydantic validation error into a readable message."""
    errors = []
    for err in error.errors():
        field = err["loc"][0] if err["loc"] else "unknown"
        msg = err["msg"]

        # Simplify common error messages
        if "Input should be a valid string" in msg and err.get("input") is None:
            errors.append(f"Le champ '{field}' est requis")
        elif "Input should be greater than or equal to" in msg:
            errors.append(f"Le champ '{field}' doit être >= {err['ctx']['ge']}")
        elif "Input should be a valid boolean" in msg:
            errors.append(f"Le champ '{field}' doit être Oui/Non")
        elif "Date must be in DD/MM/YYYY format" in msg:
            errors.append(f"Le champ '{field}' doit être au format JJ/MM/AAAA")
        else:
            errors.append(f"Erreur dans '{field}': {msg}")

    return " | ".join(errors)


class LoadDocumentsView(APIView):
    """API endpoint to trigger document loading."""

    def post(self, request):
        """Trigger document loading process."""
        document_type_str = request.data.get("type", "CORPS")

        try:
            document_type = DocumentType[document_type_str.upper()]
        except KeyError:
            raise InvalidDocumentTypeError(document_type_str) from None

        container = IngestionContainerSingleton.get_container()

        usecase = container.load_documents_usecase()
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": document_type},
        )
        result = usecase.execute(input_data)

        created_count = result["created"]
        updated_count = result["updated"]
        message = f"{created_count} documents created, {updated_count} updated"
        return Response(
            {
                "status": "success",
                "document_type": document_type.value,
                "created": result["created"],
                "updated": result["updated"],
                "message": message,
            },
            status=status.HTTP_200_OK,
        )


class ConcoursUploadView(APIView):
    """API endpoint for uploading concours CSV files."""

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """Handle CSV file upload and process concours data."""
        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES["file"]

        if not csv_file.name.endswith(".csv"):
            return Response(
                {"error": "File must be a CSV"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pl.read_csv(csv_file, separator=";")
            valid_documents = []
            validation_errors = []
            current_time = datetime.now()

            rows = df.to_dicts()

            for index, row_dict in enumerate(rows):
                try:
                    cleaned_row = {
                        k: (None if v is None else v) for k, v in row_dict.items()
                    }
                    validated_row = ConcoursRowSchema(**cleaned_row)
                    raw_data = validated_row.dict(by_alias=True)

                    # Use N° NOR as external_id for CONCOURS
                    nor_value = raw_data.get("N° NOR", "")
                    if not nor_value:
                        validation_errors.append(
                            {"row": index + 1, "error": "N° NOR manquant"}
                        )
                        continue

                    document = Document(
                        id=None,
                        external_id=nor_value,
                        raw_data=raw_data,
                        type=DocumentType.CONCOURS,
                        created_at=current_time,
                        updated_at=current_time,
                    )
                    valid_documents.append(document)

                except ValidationError as e:
                    validation_errors.append(
                        {"row": index + 1, "error": format_validation_error(e)}
                    )
                except Exception as e:
                    validation_errors.append({"row": index + 1, "error": str(e)})

            if not valid_documents:
                return Response(
                    {
                        "error": "No valid rows found",
                        "validation_errors": validation_errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            container = IngestionContainerSingleton.get_container()
            usecase = container.load_documents_usecase()
            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.UPLOAD_FROM_CSV,
                kwargs={"documents": valid_documents},
            )
            result = usecase.execute(input_data)

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
                    "validation_errors": validation_errors
                    if validation_errors
                    else None,
                },
                status=status.HTTP_201_CREATED,
            )

        except pl.exceptions.ComputeError as e:
            return Response(
                {"error": f"CSV parsing error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
