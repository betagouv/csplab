"""Mock use case for processing uploaded CV files (development only)."""

from datetime import datetime
from uuid import uuid4

from core.entities.cv_metadata import CVMetadata
from core.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from core.services.logger_interface import ILogger


class MockProcessUploadedCVUsecase:
    """Mock usecase for processing uploaded CV files without calling external APIs.

    This mock version:
    - Simulates PDF validation
    - Creates fake extracted text
    - Generates a mock search query
    - Saves real CV metadata to database

    Use TYCHO_USE_MOCK_ALBERT=1 to enable this mock.
    """

    def __init__(
        self,
        cv_metadata_repository: ICVMetadataRepository,
        logger: ILogger,
    ):
        """Initialize the mock use case.

        Args:
            cv_metadata_repository: Repository for CV metadata
            logger: Logger for tracing operations
        """
        self._cv_metadata_repository = cv_metadata_repository
        self._logger = logger.get_logger(
            "CANDIDATE::APPLICATION::MockProcessUploadedCVUsecase::execute"
        )

    def execute(self, filename: str, pdf_content: bytes) -> str:
        """Execute the mock processing of uploaded CV.

        Args:
            filename: Name of the uploaded CV file
            pdf_content: PDF file content as bytes

        Returns:
            CV ID as string

        Raises:
            ValueError: If filename or pdf_content is empty
        """
        self._logger.info(f"🎭 MOCK: Processing CV '{filename}' ({len(pdf_content)} bytes)")

        # Basic validation
        if not filename:
            raise ValueError("Filename cannot be empty")
        if not pdf_content:
            raise ValueError("PDF content cannot be empty")

        # Simulate text extraction (fake but realistic data)
        mock_extracted_text = {
            "content": """
            Jean Dupont
            Développeur Full Stack

            EXPÉRIENCE PROFESSIONNELLE
            - Développeur Senior chez TechCorp (2020-2024)
              • Développement d'applications web avec Python/Django
              • Architecture microservices
              • Gestion d'équipe de 5 développeurs

            - Développeur Junior chez StartupInc (2018-2020)
              • Développement frontend React
              • API REST avec Node.js

            FORMATION
            - Master Informatique, Université Paris-Saclay (2018)
            - Licence Informatique (2016)

            COMPÉTENCES
            Python, Django, JavaScript, React, PostgreSQL, Docker, AWS
            """,
            "pages": 2,
            "extraction_method": "mock",
        }

        # Simulate query building
        mock_search_query = "développeur full stack python django microservices"

        # Create CVMetadata entity
        cv_metadata = CVMetadata(
            id=uuid4(),
            filename=filename,
            extracted_text=mock_extracted_text,
            search_query=mock_search_query,
            created_at=datetime.now(),
        )

        # Save to database (real persistence)
        saved_cv = self._cv_metadata_repository.save(cv_metadata)

        self._logger.info(
            f"✅ MOCK: CV '{filename}' processed successfully. ID: {saved_cv.id}"
        )

        return str(saved_cv.id)
