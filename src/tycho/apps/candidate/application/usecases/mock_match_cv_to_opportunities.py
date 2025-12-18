"""Mock use case for matching CV to opportunities (development only)."""

from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from apps.candidate.infrastructure.adapters.website.fixtures.mock_opportunites import (
    MOCK_OPPORTUNITES,
)
from core.entities.concours import Concours
from core.errors.cv_errors import CVNotFoundError
from core.repositories.concours_repository_interface import IConcoursRepository
from core.repositories.cv_metadata_repository_interface import ICVMetadataRepository
from core.services.logger_interface import ILogger
from core.value_objects.access_modality import AccessModality
from core.value_objects.category import Category
from core.value_objects.ministry import Ministry
from core.value_objects.nor import NOR


class MockMatchCVToOpportunitiesUsecase:
    """Mock usecase for matching opportunities without calling embedding APIs.

    This mock version:
    - Validates CV exists
    - Returns all available concours with mock scores
    - No API calls to OpenRouter

    Use TYCHO_USE_MOCK_OPENROUTER=1 to enable this mock.
    """

    def __init__(
        self,
        cv_metadata_repository: ICVMetadataRepository,
        concours_repository: IConcoursRepository,
        logger: ILogger,
    ):
        """Initialize the mock use case.

        Args:
            cv_metadata_repository: Repository for CV metadata
            concours_repository: Repository for Concours entities
            logger: Logger for tracing operations
        """
        self._cv_metadata_repository = cv_metadata_repository
        self._concours_repository = concours_repository
        self._logger = logger.get_logger(
            "CANDIDATE::APPLICATION::MockMatchCVToOpportunitiesUsecase::execute"
        )

    def execute(self, cv_id: str, limit: int = 10) -> List[Tuple[Concours, float]]:
        """Execute mock matching - returns all concours with decreasing scores.

        Args:
            cv_id: The CV identifier
            limit: Maximum number of results to return

        Returns:
            List of tuples (Concours, relevance_score) ordered by mock relevance
        """
        self._logger.info(
            f"🎭 MOCK: Matching opportunities for cv_id='{cv_id}', limit={limit}"
        )

        cv_metadata = self._cv_metadata_repository.find_by_id(UUID(cv_id))
        if not cv_metadata:
            raise CVNotFoundError(cv_id)

        all_concours = self._concours_repository.get_all()

        # If no concours in database, create mock ones
        if not all_concours:
            self._logger.info("🎭 MOCK: No concours in database, generating mock data")
            all_concours = self._generate_mock_concours()

        concours_subset = all_concours[:limit]

        concours_with_scores = [
            (concours, max(0.50, 0.95 - (i * 0.05)))
            for i, concours in enumerate(concours_subset)
        ]

        self._logger.info(
            f"🎭 MOCK: Returning {len(concours_with_scores)} concours "
            f"with mock scores from {len(all_concours)} total"
        )

        return concours_with_scores

    def _generate_mock_concours(self) -> List[Concours]:
        """Generate mock Concours entities from fixtures data."""
        # Convert fixture dicts to Concours entities
        # Only use fixtures that are type="concours"
        concours_fixtures = [opp for opp in MOCK_OPPORTUNITES if opp.get("type") == "concours"]

        mock_concours = []
        for i, fixture in enumerate(concours_fixtures, start=1):
            # Extract category from fixture
            category_str = fixture.get("category", "A")
            category = getattr(Category, category_str, Category.A)

            # Determine access modality from type_label
            type_label = fixture.get("type_label", "")
            if "interne" in type_label.lower():
                access_modality = [AccessModality.CONCOURS_INTERNE]
            elif "externe" in type_label.lower():
                access_modality = [AccessModality.CONCOURS_EXTERNE]
            else:
                access_modality = [AccessModality.CONCOURS_EXTERNE]

            # Generate valid NOR format: [A-Z]{4}\d{7}[A-Z]
            # Example: MOCK2500001A (MOCK + year 25 + sequence 00001 + category A)
            nor_code = f"MOCK25{i:05d}{category_str}"

            concours = Concours(
                id=fixture["id"],
                nor_original=NOR(nor_code),
                nor_list=[NOR(nor_code)],
                category=category,
                ministry=Ministry.PREMIER_MINISTRE,  # Default ministry for mocks
                access_modality=access_modality,
                corps=fixture.get("intitule_poste", "Corps non spécifié"),
                grade=fixture.get("intitule_poste", "Grade non spécifié"),
                written_exam_date=datetime(2025, 6, 15),  # Mock date
                open_position_number=20,  # Mock number
            )
            mock_concours.append(concours)

        # If no concours in fixtures, generate at least one
        if not mock_concours:
            mock_concours.append(
                Concours(
                    id=999,
                    nor_original=NOR("MOCK2500001A"),
                    nor_list=[NOR("MOCK2500001A")],
                    category=Category.A,
                    ministry=Ministry.PREMIER_MINISTRE,
                    access_modality=[AccessModality.CONCOURS_EXTERNE],
                    corps="Concours de démonstration",
                    grade="Grade de démonstration",
                    written_exam_date=datetime(2025, 6, 15),
                    open_position_number=10,
                )
            )

        return mock_concours
