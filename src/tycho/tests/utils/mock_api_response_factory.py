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
        return {
            "data": [],
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
    def create_ocr_service_error_response() -> Dict:
        return {"detail": "Invalid file format or corrupted PDF"}

    @staticmethod
    def create_ocr_service_invalid_response() -> Dict:
        return {"invalid": "structure", "missing": "required_fields"}

    @staticmethod
    def create_albert_formatter_response_with_content(
        content: str, response_id: str = "chatcmpl-test123"
    ) -> Dict:
        return {
            "id": response_id,
            "object": "chat.completion",
            "created": 1774004024,
            "model": "openweight-large",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content,
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
        return MockApiResponseFactory.create_albert_formatter_response_with_content(
            json.dumps(cv_data)
        )

    @staticmethod
    def create_albert_formatter_error_response() -> Dict:
        return {
            "status_code": 401,
            "detail": "Invalid API key provided",
            "headers": {"Content-Type": "application/json"},
        }

    @staticmethod
    def create_albert_formatter_invalid_response() -> Dict:
        return {"invalid": "structure", "missing": "required_fields"}

    @staticmethod
    def create_albert_formatter_empty_choices_response() -> Dict:
        return {
            "id": "chatcmpl-test123",
            "object": "chat.completion",
            "created": 1774004024,
            "model": "openweight-large",
            "choices": [],  # Empty choices array
            "usage": {
                "prompt_tokens": 1262,
                "completion_tokens": 0,
                "total_tokens": 1262,
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

    @staticmethod
    def create_albert_formatter_fenced_json_response() -> Dict:
        cv_data = {
            "experiences": [
                {
                    "title": "Data Scientist",
                    "company": "AI Corp",
                    "sector": "Artificial Intelligence",
                    "description": "Machine learning development",
                }
            ],
            "skills": ["Python", "TensorFlow", "Pandas"],
        }

        fenced_content = f"```json\n{json.dumps(cv_data)}\n```"
        return MockApiResponseFactory.create_albert_formatter_response_with_content(
            fenced_content, "chatcmpl-test456"
        )

    @staticmethod
    def create_albert_formatter_invalid_fenced_json_response() -> Dict:
        invalid_fenced_content = '```json\n{"experiences": [invalid json here\n```'
        return MockApiResponseFactory.create_albert_formatter_response_with_content(
            invalid_fenced_content, "chatcmpl-test789"
        )
