import re
from pathlib import Path

import pytest
import yaml

from presentation.api.openapi_renderers import Yaml12SafeOpenApiRenderer

_YAML_12_INT = re.compile(r"[-+]?[0-9]+")


def _bare_digit_strings(text: str) -> list[str]:
    found = []
    pending = [yaml.compose(text, Loader=yaml.SafeLoader)]
    while pending:
        node = pending.pop()
        if isinstance(node, yaml.MappingNode):
            pending.extend(item for pair in node.value for item in pair)
        elif isinstance(node, yaml.SequenceNode):
            pending.extend(node.value)
        elif (
            node.tag == "tag:yaml.org,2002:str"
            and node.style is None
            and _YAML_12_INT.fullmatch(node.value)
        ):
            found.append(node.value)
    return found


class TestYaml12SafeOpenApiRenderer:
    def test_quotes_strings_made_of_digits(self):
        data = {"enum": ["01", "08", "09", "10", "2A", "-1"], "08": "x"}

        output = Yaml12SafeOpenApiRenderer().render(data).decode()

        assert _bare_digit_strings(output) == []
        assert yaml.safe_load(output) == data

    def test_keeps_integers_unquoted(self):
        output = Yaml12SafeOpenApiRenderer().render({"maxLength": 8}).decode()

        assert output == "maxLength: 8\n"


@pytest.mark.parametrize("filename", ["schema.yaml", "internal-schema.yaml"])
def test_committed_schema_has_no_bare_digit_string(filename):
    text = Path("presentation/static/api", filename).read_text()

    assert _bare_digit_strings(text) == []
