from typing import Literal

from django.conf import settings
from pydantic import BaseModel, HttpUrl


class OpenAIConfig(BaseModel):
    api_key: str
    base_url: HttpUrl
    embedding_model: str
    ocr_model: str


class AlbertConfig(BaseModel):
    api_base_url: HttpUrl
    api_key: str
    model: str


class PisteConfig(BaseModel):
    oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    client_id: str
    client_secret: str


class TalentsoftConfig(BaseModel):
    base_url: HttpUrl
    client_id: str
    client_secret: str


class TalentsoftBackConfig(BaseModel):
    base_url: HttpUrl
    client_id: str
    client_secret: str


class QdrantConfig(BaseModel):
    url: str | None
    api_key: str
    timeout: int = 10
    # prefer_grpc: gRPC is ~2x faster than REST for high throughput
    # See: https://qdrant.tech/documentation/interfaces/#grpc-interface
    prefer_grpc: bool = False


class OCRConfig(BaseModel):
    api_key: str
    base_url: HttpUrl


class AppConfig(BaseModel):
    # OCR
    ocr_type: Literal["ALBERT", "OPENAI"]

    # Embedding
    embedding_type: Literal["ALBERT", "OPENAI"]
    embedding_dimension: int

    # Albert
    albert_api_base_url: HttpUrl
    albert_api_key: str
    albert_model: str

    # PISTE
    piste_oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    ingres_client_id: str
    ingres_client_secret: str

    # Talentsoft
    talentsoft_base_url: HttpUrl
    talentsoft_client_id: str
    talentsoft_client_secret: str

    talentsoft_back_base_url: HttpUrl
    talentsoft_back_client_id: str
    talentsoft_back_client_secret: str

    # Qdrant
    qdrant_url: str
    qdrant_api_key: str

    # OCR Service
    ocr_api_key: str
    ocr_base_url: HttpUrl

    # Other
    opik_api_key: str

    @classmethod
    def from_django_settings(cls) -> "AppConfig":
        return cls(
            ocr_type=settings.OCR_TYPE,
            embedding_type=settings.EMBEDDING_TYPE,
            embedding_dimension=settings.EMBEDDING_DIMENSION,
            albert_api_base_url=settings.ALBERT_API_BASE_URL,
            albert_api_key=settings.ALBERT_API_KEY,
            albert_model=settings.ALBERT_MODEL,
            piste_oauth_base_url=settings.PISTE_OAUTH_BASE_URL,
            ingres_base_url=settings.INGRES_BASE_URL,
            ingres_client_id=settings.INGRES_CLIENT_ID,
            ingres_client_secret=settings.INGRES_CLIENT_SECRET,
            talentsoft_base_url=settings.TALENTSOFT_BASE_URL,
            talentsoft_client_id=settings.TALENTSOFT_CLIENT_ID,
            talentsoft_client_secret=settings.TALENTSOFT_CLIENT_SECRET,
            talentsoft_back_base_url=settings.TALENTSOFT_BACK_BASE_URL,
            talentsoft_back_client_id=settings.TALENTSOFT_BACK_CLIENT_ID,
            talentsoft_back_client_secret=settings.TALENTSOFT_BACK_CLIENT_SECRET,
            qdrant_url=settings.QDRANT_URL,
            qdrant_api_key=settings.QDRANT_API_KEY,
            ocr_api_key=settings.OCR_API_KEY,
            ocr_base_url=settings.OCR_BASE_URL,
            opik_api_key=settings.OPIK_API_KEY,
        )

    @property
    def albert(self) -> AlbertConfig:
        return AlbertConfig(
            api_base_url=self.albert_api_base_url,
            api_key=self.albert_api_key,
            model=self.albert_model,
        )

    @property
    def piste(self) -> PisteConfig:
        return PisteConfig(
            oauth_base_url=self.piste_oauth_base_url,
            ingres_base_url=self.ingres_base_url,
            client_id=self.ingres_client_id,
            client_secret=self.ingres_client_secret,
        )

    @property
    def talentsoft(self) -> TalentsoftConfig:
        return TalentsoftConfig(
            base_url=self.talentsoft_base_url,
            client_id=self.talentsoft_client_id,
            client_secret=self.talentsoft_client_secret,
        )

    @property
    def talentsoft_back(self) -> TalentsoftBackConfig:
        return TalentsoftBackConfig(
            base_url=self.talentsoft_back_base_url,
            client_id=self.talentsoft_back_client_id,
            client_secret=self.talentsoft_back_client_secret,
        )

    @property
    def qdrant(self) -> QdrantConfig:
        return QdrantConfig(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )

    @property
    def ocr(self) -> OCRConfig:
        return OCRConfig(
            api_key=self.ocr_api_key,
            base_url=self.ocr_base_url,
        )
