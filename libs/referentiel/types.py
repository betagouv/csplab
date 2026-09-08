from typing import Any, Generic, List, TypedDict, TypeVar
from uuid import UUID

from ddd.entity import Entity


class IUpsertError(TypedDict):
    entity_id: Any
    error: str
    exception: Exception


class IUpsertResult(TypedDict):
    created: int
    updated: int
    errors: List[IUpsertError]


# bound=Entity force objgeneric type to be inherited from Entity
# covariant=True allow for IBatchUpdate[T, SpecificError]
# and IBatchUpdate[T, GenericError]
# to be considered as same type if SpecificError inherits from GenericError
TEntity_co = TypeVar("TEntity_co", bound=Entity, covariant=True)
TError_co = TypeVar("TError_co", bound=Exception, covariant=True)


class IBatchUpdate(TypedDict, Generic[TEntity_co, TError_co]):
    successes: List[TEntity_co]
    failures: List[tuple[UUID, TError_co]]
