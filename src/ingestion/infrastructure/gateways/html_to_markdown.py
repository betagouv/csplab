import re
from typing import Optional
from urllib.parse import urlsplit

from markdownify import ATX, BACKSLASH, MarkdownConverter

_ALLOWED_LINK_SCHEMES = {"http", "https", "mailto"}
_URL_UNSAFE_CHARACTERS = str.maketrans({"(": "%28", ")": "%29", "<": "%3C", ">": "%3E"})
_BOLD_TAGS = {"strong", "b"}
_EXCESS_BLANK_LINES = re.compile(r"\n{3,}")
_HARD_LINE_BREAK = "\\"


class _TalentsoftMarkdownConverter(MarkdownConverter):
    """Converts the HTML of Talentsoft `Formatted` fields to CommonMark.

    - Bold, italics, lists, headings and line breaks are kept.
    - Underlines become bold (Markdown has none), unless already bold.
    - Images are dropped.
    - Tables are flattened to text; styles, classes and spans are dropped.
    - Links keep only http(s) URLs with a host and mailto with an `@`, cut at
      the first whitespace; the others become plain text.
    - Line breaks at the start or end of a block are dropped, as they would
      render as a literal backslash.
    - Markdown and HTML syntax in the text is escaped (`[clic](url)`, `![](url)`,
      decoded `&lt;script&gt;`), so that only the converted tags yield links
      and no HTML tag is ever written.
    """

    def convert_a(self, el, text, parent_tags):
        href = _clean_href(el.get("href"))
        if href is None:
            return text
        el.attrs = {"href": href}
        return super().convert_a(el, text, parent_tags)

    def convert_img(self, el, text, parent_tags):
        return ""

    def convert_u(self, el, text, parent_tags):
        already_bold = parent_tags & _BOLD_TAGS or el.find(_BOLD_TAGS)
        if already_bold:
            return text
        return self.convert_strong(el, text, parent_tags)

    def convert_table(self, el, text, parent_tags):
        return f"\n\n{text.strip()}\n\n"

    def convert_tr(self, el, text, parent_tags):
        return f"{text.strip()}\n"

    def convert_td(self, el, text, parent_tags):
        return f"{text.strip()} "

    convert_th = convert_td


def _clean_href(href: Optional[str]) -> Optional[str]:
    parts = (href or "").split()
    if not parts:
        return None
    url = parts[0]
    try:
        split = urlsplit(url)
    except ValueError:
        return None
    if split.scheme.lower() not in _ALLOWED_LINK_SCHEMES:
        return None
    if split.scheme.lower() == "mailto":
        if "@" not in split.path:
            return None
    elif not split.hostname:
        return None
    return url.translate(_URL_UNSAFE_CHARACTERS)


def _drop_dangling_line_breaks(lines: list[str]) -> list[str]:
    next_is_blank = True
    for index in reversed(range(len(lines))):
        if next_is_blank and lines[index].endswith(_HARD_LINE_BREAK):
            lines[index] = lines[index].removesuffix(_HARD_LINE_BREAK).rstrip()
        next_is_blank = not lines[index]

    previous_is_blank = True
    for index, line in enumerate(lines):
        if previous_is_blank and line == _HARD_LINE_BREAK:
            lines[index] = ""
        previous_is_blank = not lines[index]
    return lines


def html_to_markdown(html: str) -> str:
    markdown = _TalentsoftMarkdownConverter(
        autolinks=False,
        escape_misc=True,
        heading_style=ATX,
        bullets="-",
        newline_style=BACKSLASH,
    ).convert(html)
    lines = [line.rstrip(" \t\xa0") for line in markdown.splitlines()]
    markdown = "\n".join(_drop_dangling_line_breaks(lines))
    return _EXCESS_BLANK_LINES.sub("\n\n", markdown).strip(" \t\r\n\xa0")
