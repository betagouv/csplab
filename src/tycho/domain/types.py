"""Common type definitions for the domain layer."""

from typing import Union

# Using PEP 695 type alias syntax for Python 3.12+
type JsonDataType = Union[
    None,
    int,
    float,
    str,
    bool,
    list["JsonDataType"],
    dict[str, "JsonDataType"],
]
