from presentation.commons.pagination import WebPagination


def test_get_schema_operation_parameters_exposes_page_and_size():
    parameters = WebPagination().get_schema_operation_parameters(view=None)

    assert parameters == [
        {
            "name": "page",
            "required": False,
            "in": "query",
            "description": "Numéro de la page.",
            "schema": {"type": "integer"},
        },
        {
            "name": "size",
            "required": False,
            "in": "query",
            "description": "Nombre d'éléments par page.",
            "schema": {"type": "integer"},
        },
    ]


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
