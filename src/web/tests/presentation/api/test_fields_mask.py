from presentation.api.fields_mask import (
    apply_fields_mask,
    parse_fields_mask,
)


def test_parses_nested_fields():
    assert parse_fields_mask("a, b{x,y}") == {"a": None, "b": {"x": None, "y": None}}


def test_applies_the_mask_to_lists_and_objects_in_field_order():
    data = {"a": 1, "b": [{"x": 1, "y": 2}], "c": 3}

    assert apply_fields_mask(data, {"b": {"x": None}, "a": None}) == {
        "a": 1,
        "b": [{"x": 1}],
    }
