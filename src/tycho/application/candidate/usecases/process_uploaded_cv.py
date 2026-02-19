"""Use case for processing uploaded CV files."""

from datetime import datetime, timezone
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError, TextExtractionError
from domain.repositories.async_cv_metadata_repository_interface import (
    IAsyncCVMetadataRepository,
)
from domain.services.logger_interface import ILogger
from domain.services.pdf_text_extractor_interface import IPDFTextExtractor
from domain.services.query_builder_interface import IQueryBuilder
from domain.value_objects.cv_processing_status import CVStatus


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
        self._logger = logger

    async def execute(self, cv_uuid: UUID, pdf_content: bytes) -> CVMetadata:
        """Execute the processing of uploaded CV.

        Args:
            cv_uuid: UUID of the existing CV metadata
            pdf_content: PDF file content as bytes

        Returns:
            Updated CV metadata with processing results

        Raises:
            CVNotFoundError: If CV metadata not found
            TextExtractionError: If text extraction fails
        """
        self._logger.info(f"Starting CV processing for UUID: {cv_uuid}")

        # Retrieve existing CV metadata
        cv_metadata = await self._async_cv_metadata_repository.find_by_id(cv_uuid)
        if not cv_metadata:
            self._logger.error(f"CV metadata not found for UUID: {cv_uuid}")
            raise CVNotFoundError(str(cv_uuid))

        extracted_text = None
        try:
            extracted_text = await self._pdf_text_extractor.extract_text(pdf_content)
        except Exception as e:
            self._logger.error(f"Text extraction failed: {str(e)}")
            cv_metadata.status = CVStatus.FAILED
            cv_metadata.updated_at = datetime.now()
            await self._async_cv_metadata_repository.save(cv_metadata)
            raise e

        if not extracted_text or (
            not extracted_text.experiences and not extracted_text.skills
        ):
            self._logger.error("No structured content found in PDF")
            cv_metadata.status = CVStatus.FAILED
            cv_metadata.updated_at = datetime.now(timezone.utc)
            await self._async_cv_metadata_repository.save(cv_metadata)
            raise TextExtractionError(
                cv_metadata.filename, "No structured content found in PDF"
            )

        self._logger.info(
            "Text extraction successful, experiences:"
            f"{len(extracted_text.experiences)}"
            f"skills: {len(extracted_text.skills)}"
        )
        extracted_text_dict = extracted_text.model_dump()
        search_query = self._query_builder.build_query(extracted_text_dict)

        self._logger.info("Search query built successfully")

        # Update existing CV metadata
        cv_metadata.extracted_text = extracted_text_dict
        cv_metadata.search_query = search_query
        cv_metadata.status = CVStatus.COMPLETED
        cv_metadata.updated_at = datetime.now(timezone.utc)

        # Save updated CV metadata
        saved_cv = await self._async_cv_metadata_repository.save(cv_metadata)
        self._logger.info(f"CV metadata updated with status: {saved_cv.status}")
        return saved_cv
