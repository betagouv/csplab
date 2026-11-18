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
        "image": _IMG + "news/semaine-handicap.jpg",
    },
    {
        "badge": "Métier",
        "title": "Sandra Renoir, lauréate du concours de secrétaire administratif "
        "au MAASA : « Il ne faut pas hésiter à se lancer ! »",
        "url": _URL,
        "image": _IMG + "news/sandra-renoir.jpg",
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
        "image": _IMG + "news/cyril.png",
    },
    {
        "badge": "Concours",
        "title": "Cinq raisons de devenir professeur",
        "description": "Être professeur, c'est transmettre des savoirs et des "
        "valeurs, accompagner chaque élève vers la réussite et contribuer à…",
        "url": _URL,
        "image": _IMG + "news/professeur.jpg",
    },
    {
        "badge": "Événement",
        "title": "Mois de l'innovation publique 2026 : découvrez les initiatives "
        "qui transforment le service public",
        "description": "Du 2 au 30 novembre 2026, le Mois de l'innovation publique "
        "revient pour sa 13e édition. Organisé par la Direction interministérielle…",
        "url": _URL,
        "image": _IMG + "news/innovation.webp",
    },
    {
        "badge": "Concours",
        "title": "Ouverture du concours Technicien supérieur d'études et de "
        "fabrications de 3ème classe (TSEF3)",
        "description": "Vous souhaitez mettre vos compétences techniques au service "
        "de la Défense ? Exercer un métier où votre savoir-faire contribue…",
        "url": _URL,
        "image": _IMG + "news/concours-senat.png",
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
    "Guadeloupe",
    "Guyane",
    "La Réunion",
    "Martinique",
    "Mayotte",
]

_FALLBACK_PAGES = ["normandie", "pays-de-la-loire"]

_TERRITORIES = [
    ("Auvergne-Rhône-Alpes", "auvergne-rhone-alpes"),
    ("Bourgogne-Franche-Comté", "bourgogne-franche-comte"),
    ("Bretagne", "bretagne"),
    ("Centre-Val de Loire", "centre-val-de-loire"),
    ("Corse", "corse"),
    ("Grand Est", "grand-est"),
    ("Guadeloupe", "guadeloupe"),
    ("Guyane", "guyane"),
    ("Hauts-de-France", "hauts-de-france"),
    ("Île-de-France", "ile-de-france"),
    ("La Réunion", "reunion"),
    ("Martinique", "martinique"),
    ("Mayotte", "mayotte"),
    ("Normandie", "normandie"),
    ("Nouvelle-Aquitaine", "nouvelle-aquitaine"),
    ("Occitanie", "occitanie"),
    ("Pays de la Loire", "pays-de-la-loire"),
    ("Provence-Alpes-Côte d'Azur", "provence-alpes-cote-dazur"),
]


_PDL = "candidate/images/territory-pdl/"
_NOR = "candidate/images/territory-normandie/"
_TERRITORY_PAGES = {
    "pays-de-la-loire": {
        "name": "Pays de la Loire",
        "title": "La région Pays de la Loire",
        "image": _PDL + "Pays-de-la-Loire.png",
        "highlights": [
            {
                "title": "Une mobilité professionnelle en vue ? "
                "Une solution logement existe forcément !",
                "tags": ["Fonction Publique d'Etat", "Mobilité"],
                "date": "29/07/2026",
                "image": _PDL + "Visuel_Baraque.jpg",
            },
            {
                "title": "Les rencontres de l'emploi public 2026, c'est fini !",
                "tags": ["Employeur", "Événement", "Métier", "Mobilité", "Recrutement"],
                "date": "3/04/2026",
                "image": _PDL + "REP26_Zoom_16_9-400x400.jpg",
            },
            {
                "title": "Préparez votre insertion dans la fonction publique "
                "avec l'Ipag de Nantes",
                "tags": ["Candidat", "Concours"],
                "date": "3/04/2026",
                "image": _PDL + "IPAG1-400x408.jpg",
            },
            {
                "title": "Préparez votre concours administratif avec l'Ipag de Nantes",
                "tags": ["Concours"],
                "date": "3/04/2026",
                "image": _PDL + "IPAG2-400x500.jpg",
            },
        ],
        "links": [
            {
                "title": "Découvrez les grandes tendances de l'emploi public "
                "en Pays de la Loire",
                "text": "En Pays de la Loire, un fort renouvellement des effectifs "
                "à prévoir qui ouvre de beaux possibles professionnels !",
                "url": "https://www.insee.fr/fr/statistiques/8061128",
                "image": _PDL + "Image_Etude_INSEE_PDL_2024-800x450.jpg",
            },
            {
                "title": "Agents publics de l'Etat en Pays de la Loire, pour vous "
                "faciliter la vie, toute l'offre disponible en matière d'action "
                "sociale",
                "text": "Il y a forcément une prestation qui vous concerne, que vous "
                "soyez agent public de l'État, actif ou retraité, avec ou sans "
                "enfant !",
                "url": "https://srias-paysdelaloire.fr/",
                "image": _PDL + "Image_SRIAS_PDL.jpg",
            },
            {
                "title": "La Préfecture des Pays de la Loire et de Loire-Atlantique",
                "text": "Rendez-vous sur la page Linkedin de la Préfecture des Pays "
                "de la Loire et de Loire-Atlantique, chaque lundi c'est le "
                "#Monday Motivation...",
                "url": "https://www.linkedin.com/company/prefecture-de-loire-atlantique/",
                "image": _PDL + "prefecture_de_loire_atlantique_logo.jpeg",
            },
        ],
    },
    "normandie": {
        "name": "Normandie",
        "title": "La région Normandie",
        "image": _NOR + "Normandie.png",
        "highlights": [
            {
                "title": "Zoom sur la marque employeur des services de l'Etat "
                "en Normandie",
                "tags": [],
                "date": "17/08/2026",
                "image": _NOR + "Logo-4-800x450.jpg",
            },
            {
                "title": "Fonction Publique Hospitalière (FPH) : de quoi s'agit-t-il ?",
                "tags": [],
                "date": "7/05/2026",
            },
            {
                "title": "Fonction Publique Territoriale (FPT) : de quoi s'agit-t-il ?",
                "tags": [],
                "date": "7/05/2026",
            },
            {
                "title": "Fonction Publique d'État (FPE) : de quoi s'agit-t-il ?",
                "tags": [],
                "date": "7/05/2026",
            },
        ],
        "assets_title": "Nos atouts territoriaux",
        "assets": [
            {
                "title": "Un patrimoine reconnu",
                "image": _NOR + "BestJobers_NA_1110_218_HD-1200px-600x400.jpg",
                "caption": "Palais Bénédictine, Fécamp. BestJobers – "
                "Normandie Attractivité",
                "text": "La région Normandie bénéficie d'un patrimoine historique "
                "et d'une identité culturelle reconnue, portés par des sites "
                "emblématiques comme le Mont-Saint-Michel, les falaises "
                "d'Étretat, les plages du débarquement ou encore les jardins de "
                "Giverny, qui en font une région particulièrement touristique et "
                "riche. De même, les nombreux musées et centres historiques des "
                "villes composant la région représentent autant de lieux "
                "différents à découvrir.",
            },
            {
                "title": "Un territoire tourné vers l'emploi et l'innovation",
                "image": _NOR + "Toshiba3-1200px-600x400.jpg",
                "caption": "Toshiba Dieppe. Logistique Seine-Normandie",
                "text": "Au-delà de son image touristique, la région Normandie est "
                "aussi une région d'activité et de production, qui bénéficie "
                "d'un tissu économique diversifié ainsi que d'une position "
                "stratégique au niveau national, notamment au niveau maritime "
                "avec les grands ports de Rouen et du Havre. Elle se distingue "
                "par ses avancées en matière technologique, notamment dans les "
                "secteurs maritimes et spatiaux, ou encore celui de la santé.",
            },
            {
                "title": "Une région à taille humaine",
                "image": _NOR
                + "Enjoyed-by-artists-Copyright-The-Explorers-1200px-600x338.jpg",
                "caption": "Veules-les-Roses. Valentin PACAUT – The Explorers",
                "text": "La région se distingue par sa capacité à proposer un cadre "
                "de vie accessible et équilibré, et une variété de paysages "
                "inégalable. Elle est composée aussi bien de grands centres "
                "urbains que de communes rurales, de littoral maritime que "
                "d'espaces verts. Ses villes moyennes et la variété de ses "
                "espaces permettent de construire des parcours de vie différents "
                "sans renoncer à la proximité des services et emplois.",
            },
            {
                "title": "Un cadre de vie de qualité",
                "image": _NOR + "Rouen-photo911.fr-62-1200px-600x400.jpg",
                "caption": "Balade en centre-ville de Rouen. Studio 911 – "
                "Normandie Attractivité",
                "text": "La Normandie séduit par sa qualité de vie, entre son "
                "patrimoine naturel et historique et ses zones d'activité. "
                "Elle dispose aussi d'une offre culturelle dense et variée, au "
                "travers d'évènements comme l'Armada, les carnavals de Rouen et "
                "de Caen ou encore ses nombreux festivals.",
            },
        ],
        "state_title": "L'administration territoriale de l'État (ATE) en région "
        "Normandie",
        "state_text": "L'administration territoriale de l'État est caractérisée par "
        "ses services déconcentrés, qui assurent le relais au niveau local des "
        "décisions prises par l'administration centrale. Placés généralement sous "
        "l'autorité d'un préfet (de région ou de département), ils veillent à la "
        "mise en œuvre des politiques nationales au niveau territorial. Retrouvez "
        "ci-dessous les différents services de l'État en région Normandie :",
        "state_links": [
            "L'organisation de l'État au sein de la région Normandie",
            "L'organisation de l'État au sein des départements",
            "L'organisation de l'État hors-périmètre ATE",
        ],
        "figures_title": "La région en chiffres",
        "figures": [
            ("29 900 km²", "de superficie totale"),
            ("≈ 3 341 312", "habitants au 1er janvier 2025 (Insee)"),
            (
                "5 départements",
                "Seine-Maritime (76), Orne (61), Eure (27), Manche (50), Calvados (14)",
            ),
            ("2 644", "communes"),
            ("5,4 %", "du territoire métropolitain"),
            ("640 km", "de côtes le long de la Manche"),
            (
                "2 grands ports",
                (
                    "maritimes du Havre et de Rouen, débouché de Paris vers le "
                    "commerce maritime mondial"
                ),
            ),
            (
                "≈ 265 064 agents publics",
                (
                    "fin 2023 : ≈ 99 203 territoriale, ≈ 104 600 État, "
                    "≈ 71 600 hospitalière"
                ),
            ),
        ],
        "employers": 2,
        "links": [
            {
                "title": "Vie Publique",
                "text": "Mieux comprendre le fonctionnement de l'administration.",
                "url": "https://www.vie-publique.fr/fiches/administration",
            },
            {
                "title": "L'annuaire du service public",
                "text": "Trouvez des informations sur n'importe quelle administration.",
                "url": "https://lannuaire.service-public.gouv.fr/",
            },
            {
                "title": "Répertoire des métiers de la fonction publique",
                "text": "Trouvez n'importe quel emploi public.",
                "url": "https://www.fonction-publique.gouv.fr/toutes-les-"
                "publications/repertoire-commun-des-metiers-de-la-fonction-publique",
            },
            {
                "title": "INSEE : panorama de l'emploi public Normandie",
                "text": "Étude sur la démographie de la fonction publique normande.",
                "url": "https://www.insee.fr/statistiques/7674091",
            },
        ],
        "links_title": "Les ressources utiles",
    },
}


class TerritoryView(TemplateView):
    template_name = "pages/territory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        territory = _TERRITORY_PAGES.get(kwargs["slug"])
        if territory is None:
            raise Http404
        context.update(
            territory=territory,
            offers_count=sum(o["region"] == territory["name"] for o in OFFERS),
            breadcrumb_data={"links": [], "current": territory["name"]},
        )
        return context


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_news"] = _FEATURED_NEWS
        context["news"] = _NEWS
        context["query"] = self.request.GET.get("q", "")
        context["location"] = self.request.GET.get("lieu", "")
        context["regions"] = _REGIONS
        context["territories"] = [
            {
                "name": name,
                "image": f"{_IMG}territories/{slug}.png",
                "page": slug
                if slug in _TERRITORY_PAGES
                else _FALLBACK_PAGES[index % len(_FALLBACK_PAGES)],
            }
            for index, (name, slug) in enumerate(_TERRITORIES)
        ]
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
