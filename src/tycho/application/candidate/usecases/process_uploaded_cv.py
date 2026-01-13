"""Use case for processing uploaded CV files."""

from datetime import datetime
from uuid import uuid4

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import InvalidPDFError, TextExtractionError
from domain.repositories.async_cv_metadata_repository_interface import (
    IAsyncCVMetadataRepository,
)
from domain.services.logger_interface import ILogger
from domain.services.pdf_text_extractor_interface import IPDFTextExtractor
from domain.services.query_builder_interface import IQueryBuilder


class ProcessUploadedCVUsecase:
    """Usecase for processing uploaded CV files and extracting metadata."""

    def __init__(
        self,
        pdf_text_extractor: IPDFTextExtractor,
        query_builder: IQueryBuilder,
        async_cv_metadata_repository: IAsyncCVMetadataRepository,
        logger: ILogger,
    ):
        """Initialize the use case with required dependencies.

        Args:
            pdf_text_extractor: Service for extracting text from PDF
            query_builder: Service for building search queries
            async_cv_metadata_repository: Async repository for CV metadata
            logger: Logger for tracing operations
        """
        self._pdf_text_extractor = pdf_text_extractor
        self._query_builder = query_builder
        self._async_cv_metadata_repository = async_cv_metadata_repository
        self._logger = logger.get_logger(
            "CANDIDATE::APPLICATION::ProcessUploadedCVUsecase::execute"
        )

    async def execute(self, filename: str, pdf_content: bytes) -> str:
        """Execute the processing of uploaded CV.

        Args:
            filename: Name of the uploaded CV file
            pdf_content: PDF file content as bytes

        Returns:
            CV ID as string

        Raises:
            InvalidPDFError: If PDF validation fails
            TextExtractionError: If text extraction fails
            QueryBuildingError: If query building fails
            CVMetadataSaveError: If CV metadata save fails
        """
        self._logger.info(f"Starting CV processing for file: {filename}")

        # Validation PDF
        if not self._pdf_text_extractor.validate_pdf(pdf_content):
            raise InvalidPDFError(filename)

        self._logger.info("PDF validation successful")

        extracted_text = await self._pdf_text_extractor.extract_text(pdf_content)

        if not extracted_text or (
            not extracted_text.experiences and not extracted_text.skills
        ):
            self._logger.error("No structured content found in PDF")
            raise TextExtractionError(filename, "No structured content found in PDF")

        self._logger.info(
            "Text extraction successful, experiences:"
            f"{len(extracted_text.experiences)}"
            f"skills: {len(extracted_text.skills)}"
        )

        # Convert CVExtractionResult to dict for query builder compatibility
        extracted_text_dict = extracted_text.model_dump()
        search_query = self._query_builder.build_query(extracted_text_dict)

        self._logger.info("Search query built successfully")

        cv_metadata = CVMetadata(
            id=uuid4(),
            filename=filename,
            extracted_text=extracted_text_dict,
            search_query=search_query,
            created_at=datetime.now(),
        )

        # Use native async repository method - no more sync_to_async wrapper!
        saved_cv = await self._async_cv_metadata_repository.save(cv_metadata)
        self._logger.info(f"CV metadata saved with ID: {saved_cv.id}")
        return str(saved_cv.id)
