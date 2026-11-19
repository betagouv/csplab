import re
import unicodedata
from itertools import groupby

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView
from markdown_it import MarkdownIt

from presentation.api.changelog_api import (
    TYPE_LABELS,
    Filters,
    entry_html,
    published_fragments,
    published_routes,
)
from presentation.editorial.models import NewsIndexPage, NewsPage, TerritoryPage
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
    "Guadeloupe",
    "Guyane",
    "La Réunion",
    "Martinique",
    "Mayotte",
]


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = NewsPage.objects.live().order_by("path")
        context["featured_news"] = news.filter(featured=True)
        context["news"] = news.filter(featured=False)
        context["news_index"] = NewsIndexPage.objects.live().first()
        context["query"] = self.request.GET.get("q", "")
        context["location"] = self.request.GET.get("lieu", "")
        context["regions"] = _REGIONS
        context["territories"] = TerritoryPage.objects.live().order_by("path")
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


def _normalize(text: str) -> str:
    text = re.sub(r"\((e|s|es)\)", "", text.lower())
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def _matches(query: str, offer: dict) -> bool:
    haystack = _normalize(f"{offer['title']} {offer['domain']}")
    return all(word.rstrip("es") in haystack for word in _normalize(query).split())


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
            if (not query or _matches(query, o))
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
            favorites=self.request.session.get("favorites", []),
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


class OfferDetailView(TemplateView):
    template_name = "pages/components/_offer_drawer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = next((o for o in OFFERS if o["id"] == kwargs["offer_id"]), None)
        if offer is None:
            raise Http404
        context["offer"] = offer
        context["favorites"] = self.request.session.get("favorites", [])
        context["missions"] = [
            "Assurer l'accueil, l'écoute et la prise en charge des usagers",
            "Participer à l'organisation et à la continuité du service",
            "Contribuer au travail d'équipe et au suivi des dossiers",
            "Rédiger les comptes rendus et assurer la traçabilité des actions",
        ]
        context["profile"] = [
            "Diplôme ou expérience en lien avec le poste",
            "Sens du service public, rigueur et capacité d'adaptation",
            "Goût du travail en équipe",
        ]
        return context


class OfferFavoriteView(View):
    def post(self, request, offer_id):
        if not request.session.get("candidate_name"):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = reverse("candidate:login")
            return response
        offer = next((o for o in OFFERS if o["id"] == offer_id), None)
        if offer is None:
            raise Http404
        favorites = request.session.get("favorites", [])
        if offer_id in favorites:
            favorites.remove(offer_id)
        else:
            favorites.append(offer_id)
        request.session["favorites"] = favorites
        return render(
            request,
            "pages/components/_favorite_button.html",
            {"offer": offer, "favorites": favorites},
        )


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
