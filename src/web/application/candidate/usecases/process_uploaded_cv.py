from datetime import datetime, timezone
from uuid import UUID

from ddd.services.logger_interface import ILogger

from domain.candidate.entities.cv_metadata import CVMetadata
from domain.candidate.exceptions.cv_errors import CVNotFoundError, TextExtractionError
from domain.candidate.repositories.async_cv_metadata_repository_interface import (
    IAsyncCVMetadataRepository,
)
from domain.candidate.services.ocr_interface import IOCR
from domain.candidate.services.query_builder_interface import IQueryBuilder
from domain.candidate.services.text_formatter_interface import ITextFormatter
from domain.candidate.value_objects.cv_processing_status import CVStatus


class ProcessUploadedCVUsecase:
    def __init__(
        self,
        ocr: IOCR,
        text_formatter: ITextFormatter,
        query_builder: IQueryBuilder,
        async_cv_metadata_repository: IAsyncCVMetadataRepository,
        logger: ILogger,
    ):
        self.ocr = ocr
        self.text_formatter = text_formatter
        self.query_builder = query_builder
        self.async_cv_metadata_repository = async_cv_metadata_repository
        self.logger = logger

    async def execute(self, cv_uuid: UUID, pdf_content: bytes) -> CVMetadata:
        self.logger.info("Starting CV processing for UUID: %s", cv_uuid)

        # Retrieve existing CV metadata
        cv_metadata = await self.async_cv_metadata_repository.get_by_id(cv_uuid)
        if not cv_metadata:
            self.logger.error("CV metadata not found for UUID: %s", cv_uuid)
            raise CVNotFoundError(str(cv_uuid))

        extracted_text = None
        try:
            extracted_text = await self.ocr.extract_text(pdf_content)
        except Exception as e:
            self.logger.error("Text extraction failed: %s", str(e))
            cv_metadata.status = CVStatus.FAILED
            cv_metadata.updated_at = datetime.now(timezone.utc)
            await self.async_cv_metadata_repository.save(cv_metadata)
            raise e

        try:
            formatted_text = await self.text_formatter.format_text(extracted_text)
        except Exception as e:
            self.logger.error("Text formatting failed: %s", str(e))
            cv_metadata.status = CVStatus.FAILED
            cv_metadata.updated_at = datetime.now(timezone.utc)
            await self.async_cv_metadata_repository.save(cv_metadata)
            raise e

        if not formatted_text or (
            not formatted_text.experiences and not formatted_text.skills
        ):
            self.logger.error("No structured content found in PDF")
            cv_metadata.status = CVStatus.FAILED
            cv_metadata.updated_at = datetime.now(timezone.utc)
            await self.async_cv_metadata_repository.save(cv_metadata)
            raise TextExtractionError(
                cv_metadata.filename, "No structured content found in PDF"
            )

        self.logger.info(
            "Text extraction successful, experiences: %d, skills: %d",
            len(formatted_text.experiences),
            len(formatted_text.skills),
        )
        formatted_text_dict = formatted_text.model_dump()
        search_query = self.query_builder.build_query(formatted_text_dict)

        self.logger.info("Search query built successfully")

        # Update existing CV metadata
        cv_metadata.extracted_text = formatted_text_dict
        cv_metadata.search_query = search_query
        cv_metadata.status = CVStatus.COMPLETED
        cv_metadata.updated_at = datetime.now(timezone.utc)

        # Save updated CV metadata
        saved_cv = await self.async_cv_metadata_repository.save(cv_metadata)
        self.logger.info("CV metadata updated with status: %s", saved_cv.status)
        return saved_cv
