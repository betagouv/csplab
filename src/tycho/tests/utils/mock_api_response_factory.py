import json
from typing import Dict

from django.conf import settings


class MockApiResponseFactory:
    @staticmethod
    def create_empty_response() -> Dict:
        return {
            "experiences": [],
            "skills": [],
        }

    @staticmethod
    def create_albert_embedding_response(
        embedding_dimension: int = settings.EMBEDDING_DIMENSION,
        embedding_value: float = 0.1,
    ) -> Dict:
        return {
            "data": [
                {
                    "embedding": [embedding_value] * embedding_dimension,
                    "index": 0,
                    "object": "embedding",
                }
            ],
            "model": "openweight-embeddings",
            "object": "list",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 0,
                "total_tokens": 10,
                "cost": 0.001,
                "carbon": {"kWh": {"total": 0.0001}, "kgCO2eq": {"total": 0.00001}},
                "requests": 1,
            },
            "id": "test-embedding-id",
        }

    @staticmethod
    def create_albert_embedding_response_empty_data() -> Dict:
        """Create a valid Albert response structure but with empty data array."""
        return {
            "data": [],  # Empty data array
            "model": "openweight-embeddings",
            "object": "list",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 0,
                "total_tokens": 10,
                "cost": 0.001,
                "carbon": {"kWh": {"total": 0.0001}, "kgCO2eq": {"total": 0.00001}},
                "requests": 1,
            },
            "id": "test-embedding-id",
        }

    @staticmethod
    def create_openai_embedding_response(
        embedding_dimension: int = settings.EMBEDDING_DIMENSION,
        embedding_value: float = 0.1,
    ) -> Dict:
        return {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "embedding": [embedding_value] * embedding_dimension,
                    "index": 0,
                }
            ],
            "model": "text-embedding-3-small",
            "usage": {"prompt_tokens": 10, "total_tokens": 10},
        }

    @staticmethod
    def create_ocr_service_response() -> Dict:
        return {
            "text": "Software Engineer at Tech Corp. Python, Django experience.",
            "pages": 1,
        }

    @staticmethod
    def create_albert_formatter_response() -> Dict:
        cv_data = {
            "experiences": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "sector": "Technology",
                    "description": "Python development",
                }
            ],
            "skills": ["Python", "Django"],
        }

        return {
            "id": "chatcmpl-test123",
            "object": "chat.completion",
            "created": 1774004024,
            "model": "openweight-large",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": json.dumps(cv_data),
                        "refusal": None,
                        "annotations": None,
                        "audio": None,
                        "function_call": None,
                        "tool_calls": [],
                        "reasoning": None,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 1262,
                "completion_tokens": 432,
                "total_tokens": 1694,
                "cost": 0.0,
                "carbon": {
                    "kWh": {"min": 0.022736131127999996, "max": 0.026871822072},
                    "kgCO2eq": {
                        "min": 0.013437987405148953,
                        "max": 0.015880021922380184,
                    },
                },
                "requests": 1,
            },
        }
