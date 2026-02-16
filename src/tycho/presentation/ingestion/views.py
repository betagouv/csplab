"""Views for ingestion API endpoints."""

from datetime import datetime

import polars as pl
from pydantic import ValidationError
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.schemas import ConcoursRowSchema


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


class ConcoursUploadView(APIView):
    """API endpoint for uploading concours CSV files."""

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """Handle CSV file upload and process concours data."""
        container = create_ingestion_container()
        logger = container.logger_service()

        file_name = (
            request.FILES.get("file", {}).name if "file" in request.FILES else "no file"
        )
        logger.info(f"CSV upload request received: {file_name}")

        if "file" not in request.FILES:
            logger.warning("No file provided in upload request")
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES["file"]
        logger.info(f"Processing CSV file: {csv_file.name} ({csv_file.size} bytes)")

        if not csv_file.name.endswith(".csv"):
            logger.warning(f"Invalid file type: {csv_file.name}")
            return Response(
                {"error": "File must be a CSV"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pl.read_csv(csv_file, separator=";")
            valid_documents = []
            validation_errors = []
            current_time = datetime.now()

            rows = df.to_dicts()
            logger.info(f"CSV parsed successfully: {len(rows)} rows found")

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

            if not valid_documents:
                logger.warning("No valid documents found after validation")
                return Response(
                    {
                        "error": "No valid rows found",
                        "validation_errors": validation_errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            logger.info(
                f"Executing load documents usecase with {len(valid_documents)} "
                "documents"
            )
            usecase = container.load_documents_usecase()
            input_data = LoadDocumentsInput(
                operation_type=LoadOperationType.UPLOAD_FROM_CSV,
                kwargs={
                    "documents": valid_documents,
                    "document_type": DocumentType.CONCOURS,
                },
            )
            result = usecase.execute(input_data)

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
                    "validation_errors": validation_errors
                    if validation_errors
                    else None,
                },
                status=status.HTTP_201_CREATED,
            )

        except pl.exceptions.ComputeError as e:
            logger.error(f"CSV parsing error: {str(e)}")
            return Response(
                {"error": "CSV parsing error"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected error during CSV upload: {str(e)}")
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
