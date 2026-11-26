import re
from html import escape
from itertools import groupby

from django.conf import settings
from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import TemplateView
from markdown_it import MarkdownIt
from markdown_it.token import Token

from presentation.api.changelog_api import (
    TYPE_LABELS,
    Filters,
    entry_html,
    published_fragments,
    published_routes,
    title_html,
)

_TOC_MAX_LEVEL = 3
_MARKDOWN_TOC_TITLE = "Sommaire"
_ROUTE = re.compile(r"^(GET|POST|PUT|PATCH|DELETE) (/\S*)$")
_METHOD_BADGES = {
    "GET": "fr-badge--info",
    "POST": "fr-badge--success",
    "PUT": "fr-badge--warning",
    "PATCH": "fr-badge--warning",
    "DELETE": "fr-badge--error",
}

_markdown = MarkdownIt("commonmark", {"html": False}).enable("table")


def _wrap_dsfr_tables(html: str) -> str:
    html = re.sub(
        r"<table>",
        '<div class="fr-table"><div class="fr-table__wrapper">'
        '<div class="fr-table__container"><div class="fr-table__content"><table>',
        html,
    )
    return html.replace("</table>", "</table></div></div></div></div>")


def _unique_id(slug: str, used_ids: set[str]) -> str:
    anchor = slug
    suffix = 0
    while anchor in used_ids or not anchor:
        suffix += 1
        anchor = f"{slug}_{suffix}"
    used_ids.add(anchor)
    return anchor


def _add_heading_ids_and_dsfr_classes(tokens: list) -> list[dict]:
    """Adds anchors and DSFR classes to headings, returns the side menu items."""
    used_ids: set[str] = set()
    menu: list[dict] = []
    parents: list[tuple[int, list[dict]]] = [(0, menu)]
    title_seen = False
    for index, token in enumerate(tokens):
        if token.type == "hr":
            token.attrSet("class", "fr-hr fr-my-4w")
        if token.type == "blockquote_open":
            token.attrSet("class", "fr-callout fr-my-3w")
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
        is_title = level == 1 and not title_seen
        title_seen = True
        if is_title:
            continue
        while parents[-1][0] >= level:
            parents.pop()
        item: dict = {"label": label, "link": f"#{anchor}"}
        parents[-1][1].append(item)
        parents.append((level, item.setdefault("items", [])))
    _drop_empty_items(menu)
    return menu


def _drop_markdown_toc(tokens: list) -> list:
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and (
            tokens[index + 1].content == _MARKDOWN_TOC_TITLE
        ):
            end = next(
                (
                    end
                    for end in range(index + 1, len(tokens))
                    if tokens[end].type == "heading_open"
                    and tokens[end].tag <= token.tag
                ),
                len(tokens),
            )
            return tokens[:index] + tokens[end:]
    return tokens


def _route_badge(content: str) -> Token | None:
    match = _ROUTE.match(content)
    if match is None:
        return None
    method, path = match.groups()
    badge = Token("html_inline", "", 0)
    badge.content = (
        f'<span class="fr-badge fr-badge--sm fr-badge--no-icon '
        f'{_METHOD_BADGES[method]}">{method}</span> <code>{escape(path)}</code>'
    )
    return badge


def _add_route_badges(tokens: list) -> None:
    container = None
    for token in tokens:
        if token.type in ("heading_open", "th_open", "td_open"):
            container = token.type
        elif token.type in ("heading_close", "th_close", "td_close"):
            container = None
        elif token.type == "inline" and container and token.children:
            token.children = [
                _route_badge(child.content) or child
                if child.type == "code_inline"
                and (container == "heading_open" or position == 0)
                else child
                for position, child in enumerate(token.children)
            ]


def _render_guide(text: str) -> tuple[str, list[dict]]:
    tokens = _drop_markdown_toc(_markdown.parse(text))
    toc_items = _add_heading_ids_and_dsfr_classes(tokens)
    _add_route_badges(tokens)
    html = _markdown.renderer.render(tokens, _markdown.options, {})
    return _wrap_dsfr_tables(html), toc_items


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
        context["content"], context["toc_items"] = _render_guide(
            (settings.STATIC_DIR / "api" / "guide_api.md").read_text()
        )
        return context


_BADGES = {
    "non_retrocompatible": "fr-badge--error",
    "ajoute": "fr-badge--new",
    "modifie": "fr-badge--info",
    "corrige": "fr-badge--success",
    "retire": "fr-badge--warning",
}


class ApiChangelogView(TemplateView):
    template_name = "pages/api_changelog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = published_fragments()
        routes = published_routes()
        filters = Filters.from_query(self.request.GET, routes)
        fragments = filters.apply(published)
        query = filters.query_string()
        context.update(
            filters=filters,
            types=[
                {"value": t, "label": label, "checked": t in filters.types}
                for t, label in TYPE_LABELS.items()
            ],
            routes=routes,
            count=len(fragments),
            total=len(published),
            query=f"?{query}" if query else "",
            days=[
                {
                    "date": day,
                    "entries": [
                        {
                            "slug": fragment.slug,
                            "titre": title_html(fragment),
                            "label": TYPE_LABELS[fragment.type],
                            "badge": _BADGES[fragment.type],
                            "html": entry_html(fragment, new_tab=True),
                        }
                        for fragment in day_fragments
                    ],
                }
                for day, day_fragments in groupby(fragments, key=lambda f: f.date)
            ],
        )
        return context


def llms_txt(request):
    def url(path: str) -> str:
        return request.build_absolute_uri(path)

    content = f"""\
# CSPLab

> API publique de CSPLab, plateforme de recrutement de la fonction publique : offres
> d'emploi, organismes et métiers, en lecture et en écriture pour les partenaires.

Les documents ci-dessous sont en français. Le guide décrit les règles métier de
chaque route et de chaque champ ; le schéma OpenAPI fait foi en cas de divergence.

## Documentation de l'API

- [Guide de l'API]({url(reverse("api:guide_markdown"))}): règles métier des routes \
et des champs, en Markdown
- [Schéma OpenAPI]({url(static("api/schema.yaml"))}): référence technique des routes
- [Changelog]({url(reverse("api:changelog_markdown"))}): changements de l'API, du plus \
récent au plus ancien, en Markdown. Filtres : `type` (répétable : \
{", ".join(TYPE_LABELS)}), `route` (ex. `POST /api/v1/offres/creer_modifier`), \
`depuis` (AAAA-MM-JJ)
- [Changelog en JSON]({url(reverse("api:changelog_json"))}): une entrée par \
changement, avec ses routes, sa PR et ses tickets ; mêmes filtres

## Optional

- [Flux Atom du changelog]({url(reverse("api:changelog_atom"))})
- [Documentation Redoc]({url(reverse("api:redoc"))})
- [Page du changelog]({url(reverse("pages:api_changelog"))})
"""
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def security_txt(request):
    content = (
        f"Contact: mailto:{settings.SECURITY_CONTACT_EMAIL}\n"
        "Preferred-Languages: fr, en\n"
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
