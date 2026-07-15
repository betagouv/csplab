from presentation.commons.pagination import WebPagination


def test_get_paginated_response_schema_wraps_results():
    results_schema = {"type": "string"}

    schema = WebPagination().get_paginated_response_schema(results_schema)

    assert schema == {
        "type": "object",
        "required": ["count", "results"],
        "properties": {
            "count": {"type": "integer", "example": 1},
            "next": {
                "type": "string",
                "format": "uri",
                "nullable": True,
                "example": None,
            },
            "previous": {
                "type": "string",
                "format": "uri",
                "nullable": True,
                "example": None,
            },
            "results": results_schema,
        },
    }
