"""Factory for creating mock API responses for testing."""

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
