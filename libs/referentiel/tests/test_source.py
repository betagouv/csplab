from uuid import uuid4

import pytest

from referentiel.entities.source import Source
from referentiel.exceptions.source_errors import MissingTalentsoftFieldsError
from referentiel.value_objects.source_type import SourceType


@pytest.mark.parametrize(
    "client_id_front, client_id_back, base_url_front, base_url_back",
    [
        (None, "back", "https://front.example.com", "https://back.example.com"),
        ("front", None, "https://front.example.com", "https://back.example.com"),
        ("front", "back", None, "https://back.example.com"),
        ("front", "back", "https://front.example.com", None),
        (None, None, None, None),
    ],
)
def test_source_talentsoft_raises_when_fields_missing(
    client_id_front, client_id_back, base_url_front, base_url_back
):
    with pytest.raises(MissingTalentsoftFieldsError):
        Source(
            source_id=uuid4(),
            slug="talentsoft",
            type=SourceType.TALENTSOFT,
            client_id_front=client_id_front,
            client_id_back=client_id_back,
            base_url_front=base_url_front,
            base_url_back=base_url_back,
        )


def test_source_api_does_not_require_fields():
    source = Source(
        source_id=uuid4(),
        slug="api",
        type=SourceType.API,
    )
    assert source.client_id_front is None
    assert source.client_id_back is None
    assert source.base_url_front is None
    assert source.base_url_back is None
