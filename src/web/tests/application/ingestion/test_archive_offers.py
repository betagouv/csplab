from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from infrastructure.factories.referentiel.offer_factory import OfferFactory


class TestArchiveOffers:
    def setup_mocks(
        self,
        archive_offers_usecase,
        *,
        archived_ids=None,
        known_offers=None,
        vector_result=None,
        archived_count=0,
        gateway_error=None,
        get_by_ids_error=None,
        delete_vectors_error=None,
        mark_archived_error=None,
    ):
        archive_offers_usecase.document_gateway.get_archived_documents_by_period = (
            AsyncMock(return_value=archived_ids or [], side_effect=gateway_error)
        )
        archive_offers_usecase.offers_repository.get_by_external_ids = MagicMock(
            return_value=known_offers or [], side_effect=get_by_ids_error
        )
        archive_offers_usecase.vector_repository.delete_vectorized_documents = (
            MagicMock(
                return_value=vector_result or {"deleted": 0, "errors": []},
                side_effect=delete_vectors_error,
            )
        )
        archive_offers_usecase.offers_repository.mark_as_archived = MagicMock(
            return_value=archived_count, side_effect=mark_archived_error
        )

    @pytest.mark.parametrize(
        "archived_ids, known_offers",
        [
            pytest.param([], [], id="no_external_ids_fetched"),
            pytest.param(
                ["FPE-123", "FPT-456", "FPH-789"],
                [],
                id="fetched_external_ids_do_not_match_with_known_offers",
            ),
            pytest.param(
                ["FPE-123"],
                [OfferFactory.create_entity(archived_at=datetime.now())],
                id="offer_is_already_archived",
            ),
        ],
    )
    def test_usecase_returns_empty_result_when_nothing_to_archive(
        self,
        archive_offers_usecase,
        archived_ids,
        known_offers,
    ):
        self.setup_mocks(
            archive_offers_usecase, archived_ids=archived_ids, known_offers=known_offers
        )

        result = archive_offers_usecase.execute(updated_after=datetime.now())

        expected_result = {
            "fetched": len(archived_ids),
            "vector_deleted": 0,
            "entity_archived": 0,
            "errors": [],
        }
        assert result == expected_result

    def test_fetched_external_ids_are_archived(self, archive_offers_usecase):
        self.setup_mocks(
            archive_offers_usecase,
            archived_ids=["FPE-123", "FPT-456"],
            known_offers=[OfferFactory.create_entity(), OfferFactory.create_entity()],
            vector_result={"deleted": 2, "errors": []},
            archived_count=2,
        )

        result = archive_offers_usecase.execute(updated_after=datetime.now())

        assert result == {
            "fetched": 2,
            "vector_deleted": 2,
            "entity_archived": 2,
            "errors": [],
        }

    def test_delete_vectorized_documents_returns_errors(self, archive_offers_usecase):
        errors = ["Error deleting document d2d33b4d-da7d-4cac-bd51-59e76d3b45a2: msg"]
        self.setup_mocks(
            archive_offers_usecase,
            archived_ids=["FPE-123", "FPT-456"],
            known_offers=[OfferFactory.create_entity(), OfferFactory.create_entity()],
            vector_result={"deleted": 1, "errors": errors},
            archived_count=2,
        )

        result = archive_offers_usecase.execute(updated_after=datetime.now())

        assert result == {
            "fetched": 2,
            "vector_deleted": 1,
            "entity_archived": 2,
            "errors": errors,
        }

    @pytest.mark.parametrize(
        "errors, error_msg",
        [
            pytest.param(
                {"gateway_error": Exception("gateway error")},
                "gateway error",
                id="gateway_raises",
            ),
            pytest.param(
                {"get_by_ids_error": Exception("db error")},
                "db error",
                id="get_by_ids_raises",
            ),
            pytest.param(
                {"delete_vectors_error": Exception("client timeout")},
                "client timeout",
                id="delete_vectors_raises",
            ),
            pytest.param(
                {"mark_archived_error": Exception("db error")},
                "db error",
                id="mark_archived_raises",
            ),
        ],
    )
    def test_execute_propagates_exceptions(
        self, archive_offers_usecase, errors, error_msg
    ):
        self.setup_mocks(
            archive_offers_usecase,
            archived_ids=["FPE-123"],
            known_offers=[OfferFactory.create_entity()],
            vector_result={"deleted": 1, "errors": []},
            archived_count=1,
            **errors,
        )

        with pytest.raises(Exception, match=error_msg):
            archive_offers_usecase.execute(updated_after=datetime.now())
