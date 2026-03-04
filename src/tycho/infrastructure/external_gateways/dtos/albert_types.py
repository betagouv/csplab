"""Shared Albert API types and DTOs."""

from typing import Dict, List

from pydantic import BaseModel


class AlbertUsageCarbon(BaseModel):
    kWh: Dict[str, float]
    kgCO2eq: Dict[str, float]


class AlbertUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    carbon: AlbertUsageCarbon
    requests: int


class AlbertEmbeddingData(BaseModel):
    embedding: List[float]
    index: int
    object: str


class AlbertEmbeddingResponse(BaseModel):
    data: List[AlbertEmbeddingData]
    model: str
    object: str
    usage: AlbertUsage
    id: str


class AlbertDocumentPageMetadata(BaseModel):
    document_name: str
    page: int


class AlbertDocumentPage(BaseModel):
    object: str
    content: str
    images: Dict[str, str]
    metadata: AlbertDocumentPageMetadata


class AlbertOCRResponse(BaseModel):
    object: str
    data: List[AlbertDocumentPage]
    usage: AlbertUsage
