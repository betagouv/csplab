import pytest

from presentation.api.fields_mask import (
    InvalidFieldsMask,
    apply_fields_mask,
    parse_fields_mask,
    resolve_fields_mask,
)

ALLOWED = {"a": None, "b": frozenset({"x", "y"})}


def test_parses_nested_fields():
    assert parse_fields_mask("a, b{x,y}") == {"a": None, "b": {"x": None, "y": None}}


def test_star_selects_every_field_and_subfield():
    assert resolve_fields_mask(parse_fields_mask("*"), ALLOWED) == {
        "a": None,
        "b": None,
    }
    assert resolve_fields_mask(parse_fields_mask("b{*}"), ALLOWED) == {"b": None}


def test_refuses_nested_fields_deeper_than_one_level():
    with pytest.raises(InvalidFieldsMask, match="b.x"):
        resolve_fields_mask(parse_fields_mask("b{x{z}}"), ALLOWED)


def test_applies_the_mask_to_lists_and_objects_in_field_order():
    data = {"a": 1, "b": [{"x": 1, "y": 2}], "c": 3}

    assert apply_fields_mask(data, {"b": {"x": None}, "a": None}) == {
        "a": 1,
        "b": [{"x": 1}],
    }
