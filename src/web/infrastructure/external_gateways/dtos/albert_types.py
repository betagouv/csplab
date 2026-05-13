from typing import Dict, List, Optional

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


class AlbertCompletionMessage(BaseModel):
    role: str
    content: Optional[str] = None
    refusal: Optional[str] = None
    annotations: Optional[str] = None
    audio: Optional[str] = None
    function_call: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    reasoning: Optional[str] = None


class AlbertCompletionChoice(BaseModel):
    index: int
    message: AlbertCompletionMessage
    finish_reason: str


class AlbertCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[AlbertCompletionChoice]
    usage: AlbertUsage


class AlbertErrorResponse(BaseModel):
    status_code: Optional[int]
    detail: str
    headers: Optional[Dict[str, str]] | None = None
