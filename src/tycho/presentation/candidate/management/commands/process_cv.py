"""Django management command to process a CV file."""

import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from domain.exceptions.cv_errors import CVError
from infrastructure.di.candidate.candidate_factory import create_candidate_container


class Command(BaseCommand):
    help = "Process a CV PDF file using ProcessUploadedCVUsecase"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = create_candidate_container()
        self.logger = self.container.logger_service()

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "pdf_file",
            type=str,
            help="Path to the PDF file to process",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed output including extracted data",
        )

    def handle(self, *args, **options):
        pdf_file_path = options["pdf_file"]
        verbose = options["verbose"]

        if not os.path.exists(pdf_file_path):
            raise CommandError(f"File not found: {pdf_file_path}")

        if not pdf_file_path.lower().endswith(".pdf"):
            raise CommandError(f"File must be a PDF: {pdf_file_path}")

        filename = Path(pdf_file_path).name

        try:
            with open(pdf_file_path, "rb") as f:
                pdf_content = f.read()

            self.logger.info("Processing CV: %s", filename)
            self.logger.info("File size: %d bytes", len(pdf_content))

            usecase = self.container.process_uploaded_cv_usecase()

            cv_id = usecase.execute(filename, pdf_content)

            self.logger.info("CV processed successfully! CV ID: %s", cv_id)

            if verbose:
                cv_repo = self.container.postgres_cv_metadata_repository()
                cv_metadata = cv_repo.get_by_id(cv_id)

                if cv_metadata:
                    self.logger.info("Extracted data:")
                    self.logger.info(
                        json.dumps(
                            cv_metadata.extracted_text, indent=2, ensure_ascii=False
                        )
                    )
                    self.logger.info("Search query: %s", cv_metadata.search_query)
                    self.logger.info("Created at: %s", cv_metadata.created_at)

        except CVError as e:
            raise CommandError(f"CV processing error: {e}") from e
        except FileNotFoundError:
            raise CommandError(f"File not found: {pdf_file_path}") from None
        except PermissionError:
            raise CommandError(
                f"Permission denied reading file: {pdf_file_path}"
            ) from None
        except Exception as e:
            raise CommandError(f"Unexpected error: {e}") from e
