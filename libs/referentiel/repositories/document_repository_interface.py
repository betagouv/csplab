from typing import Any, List, TypedDict


class IUpsertError(TypedDict):
    entity_id: Any
    error: str
    exception: Exception


class IUpsertResult(TypedDict):
    created: int
    updated: int
    errors: List[IUpsertError]
