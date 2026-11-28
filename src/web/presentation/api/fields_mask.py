import re

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
