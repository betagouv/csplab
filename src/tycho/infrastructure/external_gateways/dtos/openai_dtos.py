"""OpenAI API response DTOs."""

from typing import List, Optional

from pydantic import BaseModel


class OpenAIMessage(BaseModel):
    """OpenAI message structure."""

    content: Optional[str] = None


class OpenAIChoice(BaseModel):
    """OpenAI choice structure."""

    message: OpenAIMessage


class OpenAIResponse(BaseModel):
    """OpenAI API response structure."""

    choices: List[OpenAIChoice]
