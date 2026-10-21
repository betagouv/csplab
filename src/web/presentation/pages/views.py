import re

from django.conf import settings
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.generic import TemplateView
from markdown_it import MarkdownIt

_TOC_MAX_LEVEL = 3

_markdown = MarkdownIt("commonmark", {"html": False}).enable("table")


def _wrap_dsfr_tables(html: str) -> str:
    html = re.sub(
        r"<table>",
        '<div class="fr-table"><div class="fr-table__wrapper">'
        '<div class="fr-table__container"><div class="fr-table__content"><table>',
        html,
    )
    return html.replace("</table>", "</table></div></div></div></div>")


def _strip_sommaire_section(markdown_text: str) -> str:
    return re.sub(
        r"^## Sommaire\n.*?\n---\n",
        "",
        markdown_text,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )


def _unique_id(slug: str, used_ids: set[str]) -> str:
    candidate = slug
    suffix = 0
    while candidate in used_ids or not candidate:
        suffix += 1
        candidate = f"{slug}_{suffix}"
    used_ids.add(candidate)
    return candidate


def _add_heading_ids_and_dsfr_classes(tokens: list) -> list[dict]:
    """Adds anchors and DSFR classes to headings, returns the side menu items."""
    used_ids: set[str] = set()
    menu: list[dict] = []
    parents: list[tuple[int, list[dict]]] = [(0, menu)]
    for index, token in enumerate(tokens):
        if token.type == "hr":
            token.attrSet("class", "fr-hr fr-my-4w")
        if token.type != "heading_open":
            continue
        level = int(token.tag[1])
        label = "".join(
            child.content
            for child in tokens[index + 1].children or []
            if child.type in ("text", "code_inline")
        )
        anchor = _unique_id(slugify(label), used_ids)
        token.attrSet("id", anchor)
        if level > _TOC_MAX_LEVEL:
            continue
        token.attrSet("class", f"fr-h{level}")
        while parents[-1][0] >= level:
            parents.pop()
        item: dict = {"label": label, "link": f"#{anchor}"}
        parents[-1][1].append(item)
        parents.append((level, item.setdefault("items", [])))
    _drop_empty_items(menu)
    return menu


def _drop_empty_items(items: list[dict]) -> None:
    for item in items:
        if item["items"]:
            _drop_empty_items(item["items"])
        else:
            del item["items"]


class HomeView(TemplateView):
    template_name = "pages/home.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"


class AccessibilityView(TemplateView):
    template_name = "pages/accessibility.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"


class LegalNoticesView(TemplateView):
    template_name = "pages/legal_notices.html"


class ApiGuideView(TemplateView):
    template_name = "pages/api_guide.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        markdown_text = _strip_sommaire_section(
            (settings.STATIC_DIR / "api" / "guide_api.md").read_text()
        )
        tokens = _markdown.parse(markdown_text)
        context["toc_items"] = _add_heading_ids_and_dsfr_classes(tokens)
        html = _markdown.renderer.render(tokens, _markdown.options, {})
        context["content"] = _wrap_dsfr_tables(html)
        return context


def security_txt(request):
    content = (
        f"Contact: mailto:{settings.SECURITY_CONTACT_EMAIL}\n"
        "Preferred-Languages: fr, en\n"
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
