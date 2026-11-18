import re
from itertools import groupby

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import TemplateView
from markdown_it import MarkdownIt

from presentation.api.changelog_api import (
    TYPE_LABELS,
    Filters,
    entry_html,
    published_fragments,
    published_routes,
)
from presentation.pages.stub_offers import OFFERS

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


def _render_guide(text: str) -> tuple[str, list[dict]]:
    tokens = _markdown.parse(text)
    toc_items = _add_heading_ids_and_dsfr_classes(tokens)
    html = _markdown.renderer.render(tokens, _markdown.options, {})
    return _wrap_dsfr_tables(html), toc_items


def _drop_empty_items(items: list[dict]) -> None:
    for item in items:
        if item["items"]:
            _drop_empty_items(item["items"])
        else:
            del item["items"]


_URL = "https://choisirleservicepublic.gouv.fr/"
_IMG = "candidate/images/"

_FEATURED_NEWS = [
    {
        "badge": "Événement",
        "title": "Semaine européenne pour l'emploi des personnes handicapées 2026 : "
        "une semaine pour favoriser l'inclusion professionnelle",
        "url": _URL,
        "image": _IMG + "service-previews/concours-card-1.png",
    },
    {
        "badge": "Métier",
        "title": "Sandra Renoir, lauréate du concours de secrétaire administratif "
        "au MAASA : « Il ne faut pas hésiter à se lancer ! »",
        "url": _URL,
        "image": _IMG + "service-previews/concours-card-2.png",
    },
]

_NEWS = [
    {
        "badge": "Diversité",
        "title": "Cyril, ancien militaire reconverti, s'engage pour l'inclusion "
        "et l'emploi des personnes en situation de handicap",
        "description": "Cyril travaille depuis près de 20 ans au ministère des "
        "Armées et des Anciens combattants : après une carrière militaire,…",
        "url": _URL,
        "image": _IMG + "illustrations-csp/scene-4.svg",
    },
    {
        "badge": "Concours",
        "title": "Cinq raisons de devenir professeur",
        "description": "Être professeur, c'est transmettre des savoirs et des "
        "valeurs, accompagner chaque élève vers la réussite et contribuer à…",
        "url": _URL,
        "image": _IMG + "illustrations-csp/parcours-professionnels-1.svg",
    },
    {
        "badge": "Événement",
        "title": "Mois de l'innovation publique 2026 : découvrez les initiatives "
        "qui transforment le service public",
        "description": "Du 2 au 30 novembre 2026, le Mois de l'innovation publique "
        "revient pour sa 13e édition. Organisé par la Direction interministérielle…",
        "url": _URL,
        "image": _IMG + "illustrations-csp/recherche-1.svg",
    },
    {
        "badge": "Concours",
        "title": "Ouverture du concours Technicien supérieur d'études et de "
        "fabrications de 3ème classe (TSEF3)",
        "description": "Vous souhaitez mettre vos compétences techniques au service "
        "de la Défense ? Exercer un métier où votre savoir-faire contribue…",
        "url": _URL,
        "image": _IMG + "illustrations-csp/recherche-emploi.svg",
    },
]


_REGIONS = [
    "Auvergne-Rhône-Alpes",
    "Bourgogne-Franche-Comté",
    "Bretagne",
    "Centre-Val de Loire",
    "Corse",
    "Grand Est",
    "Hauts-de-France",
    "Île-de-France",
    "Normandie",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Pays de la Loire",
    "Provence-Alpes-Côte d'Azur",
]


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_news"] = _FEATURED_NEWS
        context["news"] = _NEWS
        context["query"] = self.request.GET.get("q", "")
        context["location"] = self.request.GET.get("lieu", "")
        context["regions"] = _REGIONS
        return context


_DOMAINS = [
    "Médical et paramédical",
    "Social, enfance et famille",
    "Administration et gestion",
    "Numérique et systèmes d'information",
    "Éducation et formation",
]
_VERSANTS = [
    "Fonction publique Hospitalière",
    "Fonction publique Territoriale",
    "Fonction publique de l'État",
]

_OFFERS_PER_PAGE = 10


class OffersView(TemplateView):
    template_name = "pages/offers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET
        query = params.get("q", "").strip()
        location = params.get("lieu", "")
        domain = params.get("domaine", "")
        versant = params.get("structure", "")
        telework = params.get("teletravail") == "1"
        offers = [
            o
            for o in sorted(OFFERS, key=lambda o: o["since"], reverse=True)
            if (not query or query.lower() in f"{o['title']} {o['domain']}".lower())
            and (not location or o["region"] == location)
            and (not domain or o["domain"] == domain)
            and (not versant or o["versant"] == versant)
            and (not telework or o["telework"])
        ]
        page = Paginator(offers, _OFFERS_PER_PAGE).get_page(params.get("page"))
        base_params = params.copy()
        base_params.pop("page", None)
        context.update(
            breadcrumb_data={"links": [], "current": "Offres d'emploi"},
            offers=page,
            total=len(offers),
            page_query=base_params.urlencode(),
            query=query,
            location=location,
            domain=domain,
            versant=versant,
            telework=telework,
            regions=_REGIONS,
            domains=_DOMAINS,
            versants=_VERSANTS,
        )
        return context


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
