from presentation.commons.pagination import TalentsoftPagination, WebPagination


def test_get_schema_operation_parameters_exposes_page_and_size():
    parameters = WebPagination().get_schema_operation_parameters(view=None)

    assert parameters == [
        {
            "name": "page",
            "required": False,
            "in": "query",
            "description": "Numéro de la page.",
            "schema": {"type": "integer", "default": 1, "minimum": 1},
        },
        {
            "name": "taille",
            "required": False,
            "in": "query",
            "description": "Nombre d'éléments par page.",
            "schema": {
                "type": "integer",
                "default": WebPagination.page_size,
                "minimum": WebPagination.min_page_size,
            },
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


def test_talentsoft_get_schema_operation_parameters_exposes_start_and_count():
    parameters = TalentsoftPagination().get_schema_operation_parameters(view=None)

    assert parameters == [
        {
            "name": "start",
            "required": False,
            "in": "query",
            "description": "Index de début de la pagination.",
            "schema": {"type": "integer"},
        },
        {
            "name": "count",
            "required": False,
            "in": "query",
            "description": "Nombre d'éléments par page.",
            "schema": {"type": "integer"},
        },
    ]


def test_talentsoft_get_paginated_response_schema_wraps_results():
    results_schema = {"type": "string"}

    schema = TalentsoftPagination().get_paginated_response_schema(results_schema)

    assert schema == {
        "type": "object",
        "required": ["data", "_pagination"],
        "properties": {
            "data": results_schema,
            "_pagination": {
                "type": "object",
                "properties": {
                    "start": {"type": "integer", "example": 0},
                    "count": {"type": "integer", "example": 1},
                    "total": {"type": "integer", "example": 1},
                    "resultsPerPage": {"type": "integer", "example": 100},
                    "hasMore": {"type": "boolean", "example": False},
                },
            },
        },
    }
