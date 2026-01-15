"""Configuration for PDF extractors."""

from pydantic import BaseModel

from domain.value_objects.pdf_extractor_type import PDFExtractorType
from infrastructure.external_gateways.configs.albert_config import AlbertConfig
from infrastructure.external_gateways.configs.openai_config import OpenAIConfig


class PDFExtractorConfig(BaseModel):
    """Unified configuration for PDF extractors."""

    pdf_extractor_type: PDFExtractorType
    albert: AlbertConfig
    openai: OpenAIConfig

    def __init__(
        self,
        pdf_extractor_type: PDFExtractorType,
        albert_config: AlbertConfig,
        openai_config: OpenAIConfig,
    ):
        """Create unified configuration."""
        super().__init__(
            pdf_extractor_type=pdf_extractor_type,
            albert=albert_config,
            openai=openai_config,
        )
