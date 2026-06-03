from typing import Protocol

from ddd.types import JsonDataType


class IQueryBuilder(Protocol):
    def build_query(self, cv_data: JsonDataType) -> str: ...
