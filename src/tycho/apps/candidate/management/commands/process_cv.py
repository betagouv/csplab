"""Django management command to process a CV file."""

import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.candidate.container_factory import create_candidate_container
from core.errors.cv_errors import CVError


class Command(BaseCommand):
    """Django management command to process a CV PDF file."""

    help = "Process a CV PDF file using ProcessUploadedCVUsecase"

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
        """Handle the command execution."""
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

            self.stdout.write(f"Processing CV: {filename}")
            self.stdout.write(f"File size: {len(pdf_content)} bytes")

            container = create_candidate_container()
            usecase = container.process_uploaded_cv_usecase()

            cv_id = usecase.execute(filename, pdf_content)

            self.stdout.write(self.style.SUCCESS("✅ CV processed successfully!"))
            self.stdout.write(f"CV ID: {cv_id}")

            if verbose:
                cv_repo = container.cv_metadata_repository()
                cv_metadata = cv_repo.find_by_id(cv_id)

                if cv_metadata:
                    self.stdout.write("\n📄 Extracted data:")
                    self.stdout.write(
                        json.dumps(
                            cv_metadata.extracted_text, indent=2, ensure_ascii=False
                        )
                    )
                    self.stdout.write(f"\n🔍 Search query: {cv_metadata.search_query}")
                    self.stdout.write(f"📅 Created at: {cv_metadata.created_at}")

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
