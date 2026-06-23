import uuid
from unittest.mock import MagicMock

import pytest

from application.ingestion.interfaces.get_offers_by_source_input import (
    GetOffersBySourceInput,
)
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)


def test_returns_offers_when_utilisateur_is_authorized(get_offers_by_source_usecase):
    source_id = uuid.uuid4()
    utilisateur_entity_id = uuid.uuid4()
    utilisateur = MagicMock(is_superuser=False)
    page = object()

    get_offers_by_source_usecase.utilisateur_repository.get_by_entity_id = MagicMock(
        return_value=utilisateur
    )
    get_offers_by_source_usecase.user_source_repository.get_allowed_source_ids = (
        MagicMock(return_value={source_id})
    )
    get_offers_by_source_usecase.offers_repository.get_by_source_id = MagicMock(
        return_value=page
    )

    result = get_offers_by_source_usecase.execute(
        GetOffersBySourceInput(
            source_id=source_id, utilisateur_entity_id=utilisateur_entity_id
        )
    )

    assert result is page
    get_offers_by_source_usecase.utilisateur_repository.get_by_entity_id.assert_called_once_with(
        utilisateur_entity_id
    )
    get_offers_by_source_usecase.user_source_repository.get_allowed_source_ids.assert_called_once_with(
        utilisateur, {source_id}
    )
    get_offers_by_source_usecase.offers_repository.get_by_source_id.assert_called_once_with(
        source_id
    )


def test_raises_when_utilisateur_is_not_authorized(get_offers_by_source_usecase):
    source_id = uuid.uuid4()
    utilisateur_entity_id = uuid.uuid4()

    get_offers_by_source_usecase.utilisateur_repository.get_by_entity_id = MagicMock(
        return_value=MagicMock(is_superuser=False)
    )
    get_offers_by_source_usecase.user_source_repository.get_allowed_source_ids = (
        MagicMock(return_value=set())
    )
    get_offers_by_source_usecase.offers_repository.get_by_source_id = MagicMock()

    with pytest.raises(SourceAuthorizationError) as exc_info:
        get_offers_by_source_usecase.execute(
            GetOffersBySourceInput(
                source_id=source_id, utilisateur_entity_id=utilisateur_entity_id
            )
        )

    assert exc_info.value.source_ids == {source_id}
    get_offers_by_source_usecase.offers_repository.get_by_source_id.assert_not_called()


def test_returns_offers_for_superuser_without_allowed_source(
    get_offers_by_source_usecase,
):
    source_id = uuid.uuid4()
    utilisateur_entity_id = uuid.uuid4()
    page = object()

    get_offers_by_source_usecase.utilisateur_repository.get_by_entity_id = MagicMock(
        return_value=MagicMock(is_superuser=True)
    )
    get_offers_by_source_usecase.user_source_repository.get_allowed_source_ids = (
        MagicMock()
    )
    get_offers_by_source_usecase.offers_repository.get_by_source_id = MagicMock(
        return_value=page
    )

    result = get_offers_by_source_usecase.execute(
        GetOffersBySourceInput(
            source_id=source_id, utilisateur_entity_id=utilisateur_entity_id
        )
    )

    assert result is page
    get_offers_by_source_usecase.user_source_repository.get_allowed_source_ids.assert_not_called()
    get_offers_by_source_usecase.offers_repository.get_by_source_id.assert_called_once_with(
        source_id
    )
