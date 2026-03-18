import json
from typing import Dict, List, Optional

from django.conf import settings


class MockApiResponseFactory:
    @staticmethod
    def create_empty_response() -> Dict:
        return {
            "experiences": [],
            "skills": [],
        }

    @staticmethod
    def create_ocr_api_response(
        experiences: List[tuple],
        skills: Optional[List[str]] = None,
        sector: str = "Technology",
        description: str = "Professional experience",
    ) -> Dict:

        if skills is None:
            skills = ["Python", "Django"]

        xps = [
            {
                "title": title,
                "company": company,
                "sector": sector,
                "description": description,
            }
            for title, company in experiences
        ]

        return {
            "experiences": xps,
            "skills": skills,
        }

    @staticmethod
    def create_albert_ocr_response(cv_content: Dict) -> Dict:

        return {
            "object": "ocr_response",
            "data": [
                {
                    "object": "document_page",
                    "content": json.dumps(cv_content),
                    "images": {},
                    "metadata": {"document_name": "test.pdf", "page": 1},
                }
            ],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
                "cost": 0.01,
                "carbon": {"kWh": {"total": 0.001}, "kgCO2eq": {"total": 0.0001}},
                "requests": 1,
            },
        }

    @staticmethod
    def create_albert_ocr_response_with_invalid_json(invalid_json_content: str) -> Dict:

        return {
            "object": "ocr_response",
            "data": [
                {
                    "object": "document_page",
                    "content": invalid_json_content,
                    "images": {},
                    "metadata": {"document_name": "test.pdf", "page": 1},
                }
            ],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
                "cost": 0.01,
                "carbon": {"kWh": {"total": 0.001}, "kgCO2eq": {"total": 0.0001}},
                "requests": 1,
            },
        }

    @staticmethod
    def create_ocr_response_with_none_values() -> Dict:

        return {
            "experiences": [
                {
                    "title": "Développeur Senior",
                    "company": None,
                    "sector": "IT",
                    "description": "Développement web",
                },
                {
                    "title": "Chef de projet",
                    "company": "StartupXYZ",
                    "sector": None,
                    "description": None,
                },
            ],
            "skills": ["Python", "Django", "React"],
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
