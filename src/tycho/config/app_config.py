"""
Centralized application configuration.
Provides injectable configuration for dependency injection containers.
"""

from typing import Literal

from django.conf import settings
from pydantic import BaseModel, HttpUrl


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""

    api_key: str
    base_url: HttpUrl
    embedding_model: str
    ocr_model: str


class AlbertConfig(BaseModel):
    """Albert API configuration."""

    api_base_url: HttpUrl
    api_key: str
    ocr_model: str
    ocr_dpi: int


class PisteConfig(BaseModel):
    """PISTE API configuration."""

    oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    client_id: str
    client_secret: str


class TalentsoftConfig(BaseModel):
    """Talentsoft API configuration."""

    base_url: HttpUrl
    client_id: str
    client_secret: str


class AppConfig(BaseModel):
    """
    Application configuration for dependency injection.
    Centralizes all external API configurations.
    """

    # OCR
    ocr_type: Literal["ALBERT", "OPENAI"]

    # OpenAI/OpenRouter
    openrouter_api_key: str
    openrouter_base_url: HttpUrl
    openrouter_embedding_model: str
    openrouter_ocr_model: str

    # Albert
    albert_api_base_url: HttpUrl
    albert_api_key: str
    albert_ocr_model: str
    albert_ocr_dpi: int

    # PISTE
    piste_oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    ingres_client_id: str
    ingres_client_secret: str

    # Talentsoft
    talentsoft_base_url: HttpUrl
    talentsoft_client_id: str
    talentsoft_client_secret: str

    # Other
    opik_api_key: str

    @classmethod
    def from_django_settings(cls) -> "AppConfig":
        """Create AppConfig from Django settings."""
        return cls(
            ocr_type=settings.OCR_TYPE,
            openrouter_api_key=settings.OPENROUTER_API_KEY,
            openrouter_base_url=settings.OPENROUTER_BASE_URL,
            openrouter_embedding_model=settings.OPENROUTER_EMBEDDING_MODEL,
            openrouter_ocr_model=settings.OPENROUTER_OCR_MODEL,
            albert_api_base_url=settings.ALBERT_API_BASE_URL,
            albert_api_key=settings.ALBERT_API_KEY,
            albert_ocr_model=settings.ALBERT_OCR_MODEL,
            albert_ocr_dpi=settings.ALBERT_OCR_DPI,
            piste_oauth_base_url=settings.PISTE_OAUTH_BASE_URL,
            ingres_base_url=settings.INGRES_BASE_URL,
            ingres_client_id=settings.INGRES_CLIENT_ID,
            ingres_client_secret=settings.INGRES_CLIENT_SECRET,
            talentsoft_base_url=settings.TALENTSOFT_BASE_URL,
            talentsoft_client_id=settings.TALENTSOFT_CLIENT_ID,
            talentsoft_client_secret=settings.TALENTSOFT_CLIENT_SECRET,
            opik_api_key=settings.OPIK_API_KEY,
        )

    @property
    def openai(self) -> OpenAIConfig:
        """Get OpenAI configuration."""
        return OpenAIConfig(
            api_key=self.openrouter_api_key,
            base_url=self.openrouter_base_url,
            embedding_model=self.openrouter_embedding_model,
            ocr_model=self.openrouter_ocr_model,
        )

    @property
    def albert(self) -> AlbertConfig:
        """Get Albert configuration."""
        return AlbertConfig(
            api_base_url=self.albert_api_base_url,
            api_key=self.albert_api_key,
            ocr_model=self.albert_ocr_model,
            ocr_dpi=self.albert_ocr_dpi,
        )

    @property
    def piste(self) -> PisteConfig:
        """Get PISTE configuration."""
        return PisteConfig(
            oauth_base_url=self.piste_oauth_base_url,
            ingres_base_url=self.ingres_base_url,
            client_id=self.ingres_client_id,
            client_secret=self.ingres_client_secret,
        )

    @property
    def talentsoft(self) -> TalentsoftConfig:
        """Get Talentsoft configuration."""
        return TalentsoftConfig(
            base_url=self.talentsoft_base_url,
            client_id=self.talentsoft_client_id,
            client_secret=self.talentsoft_client_secret,
        )
