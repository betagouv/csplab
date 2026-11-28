import re
from collections.abc import Mapping

FieldsMask = dict[str, "FieldsMask | None"]

_NAME = re.compile(r"\w+|\*")


class InvalidFieldsMask(ValueError):
    pass


def parse_fields_mask(raw: str) -> FieldsMask:
    mask, rest = _parse(re.sub(r"\s", "", raw))
    if rest or not mask:
        raise InvalidFieldsMask(f"X-Fields invalide : « {raw} ».")
    return mask


def _parse(text: str) -> tuple[FieldsMask, str]:
    mask: FieldsMask = {}
    while match := _NAME.match(text):
        text = text[match.end() :]
        submask = None
        if text.startswith("{"):
            submask, text = _parse(text[1:])
            if not text.startswith("}"):
                return mask, text
            text = text[1:]
        mask[match.group()] = submask
        if not text.startswith(",") or not _NAME.match(text[1:]):
            break
        text = text[1:]
    return mask, text


def resolve_fields_mask(
    mask: FieldsMask, allowed: Mapping[str, frozenset[str] | None]
) -> FieldsMask:
    if "*" in mask:
        mask = dict.fromkeys(allowed) | mask
        del mask["*"]
    refused = []
    for name, submask in mask.items():
        if name not in allowed:
            refused.append(name)
        elif submask is not None:
            subfields = allowed[name] or frozenset()
            refused += [
                f"{name}.{subname}"
                for subname, subsubmask in submask.items()
                if subname not in subfields | {"*"} or subsubmask is not None
            ]
    if refused:
        raise InvalidFieldsMask(
            "Champs inconnus ou non exposés dans X-Fields : " + ", ".join(refused) + "."
        )
    return {
        name: None if submask is None or "*" in submask else submask
        for name, submask in mask.items()
    }


def apply_fields_mask(data: dict, mask: FieldsMask) -> dict:
    return {
        name: _apply_submask(value, mask[name])
        for name, value in data.items()
        if name in mask
    }


def _apply_submask(value, submask: FieldsMask | None):
    if submask is None or value is None:
        return value
    if isinstance(value, list):
        return [_apply_submask(item, submask) for item in value]
    return {name: item for name, item in value.items() if name in submask}
