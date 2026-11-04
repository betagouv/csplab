import re

import yaml
from drf_spectacular.renderers import OpenApiYamlRenderer, SafeDumper

# PyYAML (YAML 1.1) leaves `08` and `09` unquoted: YAML 1.2 readers see integers.
_DIGITS_ONLY = re.compile(r"[-+]?[0-9]+")


class _QuotedStr(str):
    pass


yaml.add_representer(
    _QuotedStr,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str", str(data), style="'"
    ),
    Dumper=SafeDumper,
)


def _quote_digit_strings(data):
    if isinstance(data, dict):
        return {
            _quote_digit_strings(key): _quote_digit_strings(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [_quote_digit_strings(item) for item in data]
    if type(data) is str and _DIGITS_ONLY.fullmatch(data):
        return _QuotedStr(data)
    return data


class Yaml12SafeOpenApiRenderer(OpenApiYamlRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render(
            _quote_digit_strings(data), accepted_media_type, renderer_context
        )
