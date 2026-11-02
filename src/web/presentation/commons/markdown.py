import nh3
from django.utils.safestring import SafeString, mark_safe
from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.token import Token

_ALLOWED_TAGS = {
    "a",
    "br",
    "em",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "ol",
    "p",
    "strong",
    "ul",
}
_ALLOWED_ATTRIBUTES = {"a": {"href"}, "ol": {"start"}}
_ALLOWED_URL_SCHEMES = {"http", "https", "mailto"}
_MAX_HEADING_LEVEL = 6


def _is_allowed_link(url: str) -> bool:
    scheme, separator, _ = url.strip().partition(":")
    return bool(separator) and scheme.lower() in _ALLOWED_URL_SCHEMES


def _image(self, tokens, idx, options, env) -> str:
    return escapeHtml(self.renderInlineAsText(tokens[idx].children, options, env))


_DISABLED_RULES = ["blockquote", "code", "fence", "backticks"]
_EXCERPT_LENGTH = 50

_markdown = MarkdownIt("commonmark", {"html": False, "breaks": True}).disable(
    _DISABLED_RULES
)
_markdown.validateLink = _is_allowed_link  # type: ignore[method-assign]
_markdown.add_render_rule("image", _image)


def _shift_headings(tokens: list, top_level: int) -> None:
    """Moves headings below the page heading, keeping their relative levels."""
    headings = [token for token in tokens if token.type.startswith("heading_")]
    if not headings:
        return
    offset = top_level - min(int(token.tag[1]) for token in headings)
    for token in headings:
        level = min(int(token.tag[1]) + offset, _MAX_HEADING_LEVEL)
        token.tag = f"h{level}"


def _headings_to_bold_paragraphs(tokens: list) -> None:
    for index, token in enumerate(tokens):
        if token.type not in ("heading_open", "heading_close"):
            continue
        token.type = token.type.replace("heading", "paragraph")
        token.tag = "p"
        token.markup = ""
        if token.type == "paragraph_open":
            inline = tokens[index + 1]
            inline.children = [
                Token("strong_open", "strong", 1),
                *(inline.children or []),
                Token("strong_close", "strong", -1),
            ]


def _render(tokens: list) -> SafeString:
    html = _markdown.renderer.render(tokens, _markdown.options, {})
    # Defense in depth: markdown-it output is already safe.
    cleaned = nh3.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        url_schemes=_ALLOWED_URL_SCHEMES,
        url_relative="deny",
        link_rel="noopener noreferrer",
        set_tag_attribute_values={"a": {"target": "_blank"}},
    )
    return mark_safe(cleaned.strip())  # noqa: S308


def render_markdown(text: str | None, top_heading_level: int) -> SafeString:
    tokens = _markdown.parse(text or "")
    _shift_headings(tokens, top_heading_level)
    return _render(tokens)


def render_markdown_without_headings(text: str | None) -> SafeString:
    tokens = _markdown.parse(text or "")
    _headings_to_bold_paragraphs(tokens)
    return _render(tokens)


# Parses HTML and every link, so that they can be reported.
_permissive_markdown = MarkdownIt("commonmark", {"html": True}).disable(_DISABLED_RULES)
_permissive_markdown.validateLink = lambda url: True  # type: ignore[method-assign]


def _excerpt(text: str) -> str:
    first_line = next(iter(text.strip().splitlines()), "")
    if len(first_line) > _EXCERPT_LENGTH:
        return first_line[:_EXCERPT_LENGTH] + "…"
    return first_line


def _all_tokens(tokens: list) -> list:
    return [token for parent in tokens for token in [parent, *(parent.children or [])]]


def forbidden_markdown(text: str) -> list[str]:
    errors = []
    for token in _all_tokens(_permissive_markdown.parse(text)):
        if token.type in ("html_block", "html_inline"):
            errors.append(
                f"Les balises HTML ne sont pas acceptées ({_excerpt(token.content)}) : "
                "utilisez la syntaxe Markdown, ou écrivez \\< pour afficher "
                "le caractère <."
            )
        url = token.attrGet("href") if token.type == "link_open" else None
        if token.type == "image":
            url = token.attrGet("src")
        if url is not None and not _is_allowed_link(str(url)):
            errors.append(
                f"Lien non autorisé ({_excerpt(str(url))}) : seuls les liens "
                "http, https et mailto sont acceptés."
            )
    return errors
