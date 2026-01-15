"""Common type definitions for the domain layer."""

from typing import Dict, List, Union

from typing_extensions import TypeAlias

JsonDataType: TypeAlias = Union[
    None,
    int,
    float,
    str,
    bool,
    List["JsonDataType"],
    Dict[str, "JsonDataType"],
]
