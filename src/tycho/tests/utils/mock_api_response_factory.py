"""Factory for creating mock API responses for testing."""

import json
from typing import Dict, List, Optional


class MockApiResponseFactory:
    """Factory for creating consistent mock API responses across tests."""

    @staticmethod
    def create_empty_response() -> Dict:
        """Create a mock response with empty experiences and skills.

        Returns:
            Mock API response with empty data
        """
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
        """Create a mock response with multiple experiences.

        Args:
            experiences: List of (title, company) tuples
            skills: List of skills. Defaults to ["Python", "Django"]
            sector: Industry sector
            description: Job description

        Returns:
            Mock API response with multiple experiences
        """
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
        """Create a complete Albert OCR API response structure.

        Args:
            cv_content: The CV content (experiences and skills) to embed in the response

        Returns:
            Complete Albert OCR response structure
        """

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
        """Create Albert OCR response with invalid JSON content.

        Args:
            invalid_json_content: Invalid JSON string to embed in the response

        Returns:
            Albert OCR response structure with invalid JSON content
        """
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
        """Create a mock response with None values for company and description.

        Returns:
            Mock API response with None values that previously caused validation errors
        """
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
