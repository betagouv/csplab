import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from functools import cache
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse
from zoneinfo import ZoneInfo

import yaml
from django.conf import settings
from django.http import QueryDict
from markdown_it import MarkdownIt

FRAGMENTS_DIR = settings.STATIC_DIR / "api" / "changelog_api.d"
REPO_URL = "https://github.com/betagouv/csplab"
DATE_COMMAND = "mise run web:changelog-api:dater"
# Covers a weekend between approval and merge.
DATE_TOLERANCE = timedelta(days=3)

# Public routes outside the OpenAPI schema that a fragment may cite.
DOC_ROUTES = (
    "GET /api/changelog.md",
    "GET /api/changelog.json",
    "GET /api/changelog.atom",
    "GET /api/guide.md",
)

TYPES = {
    "non_retrocompatible": "⚠️ Changements non rétrocompatibles",
    "ajoute": "Ajouté",
    "modifie": "Modifié",
    "corrige": "Corrigé",
    "retire": "Retiré",
}

TYPE_LABELS = {
    "non_retrocompatible": "Non rétrocompatible",
    "ajoute": "Ajouté",
    "modifie": "Modifié",
    "corrige": "Corrigé",
    "retire": "Retiré",
}

HEADER = """\
Ce changelog liste les changements de l'API publique CSPLab (routes `/api/v1/…` et
`/api/fake-ts/…`) qui concernent les partenaires qui l'utilisent. Le détail des
champs et de leurs règles se trouve dans le [guide de l'API]({base}/pages/guide_api).

Il est aussi publié sur une [page filtrable]({base}/pages/changelog_api), et pour les
outils et les agents en [Markdown]({base}/api/changelog.md), en
[JSON]({base}/api/changelog.json) et en [flux Atom]({base}/api/changelog.atom).

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
"""

_FIELDS = {"type", "date", "pr", "liens"}
_DATE_FORMAT = re.compile(r"\d{4}-\d{2}-\d{2}")
_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
_SUBSECTION = re.compile(r"^### (.+)$", re.MULTILINE)
_ROUTE = re.compile(r"`((?:GET|POST|PUT|PATCH|DELETE) /api/[^`\s]*)`")
# A `{parameter}` of a path, once escaped by re.escape.
_PATH_PARAMETER = re.compile(r"\\\{[^}]+\\\}")
_GITHUB_REFERENCE = re.compile(
    rf"{re.escape(REPO_URL)}/(?:issues|pull)/(\d+)", re.IGNORECASE
)


class _StringDateLoader(yaml.SafeLoader):
    """Keeps dates as strings, to check their YYYY-MM-DD format."""


_StringDateLoader.yaml_implicit_resolvers = {
    first: [
        (tag, regexp)
        for tag, regexp in resolvers
        if tag != "tag:yaml.org,2002:timestamp"
    ]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class FragmentError(ValueError):
    def __init__(self, path: Path, errors: list[str]):
        self.path = path
        self.errors = errors
        super().__init__(f"{path.name} : {' ; '.join(errors)}")


@dataclass(frozen=True)
class Fragment:
    path: Path
    type: str
    date: date
    pr: int
    liens: tuple[str, ...]
    entry: str
    subsections: tuple[tuple[str, str], ...]
    routes: tuple[str, ...] = ()

    @property
    def slug(self) -> str:
        """Anchor and identifier of the entry: never rename a published fragment."""
        return self.path.stem

    @property
    def pr_url(self) -> str:
        return f"{REPO_URL}/pull/{self.pr}"

    @property
    def sort_key(self) -> tuple[int, int, str]:
        return (list(TYPES).index(self.type), self.pr, self.path.name)


def parse_fragment(path: Path) -> Fragment:
    match = _FRONT_MATTER.match(path.read_text())
    if match is None:
        raise FragmentError(
            path, ["en-tête YAML absent, le fichier doit commencer par `---`"]
        )
    try:
        metadata = yaml.load(match.group(1), Loader=_StringDateLoader)  # noqa: S506
    except yaml.YAMLError as error:
        raise FragmentError(path, [f"en-tête YAML invalide : {error}"]) from error
    if not isinstance(metadata, dict):
        raise FragmentError(path, ["l'en-tête YAML doit être un dictionnaire"])

    errors = _metadata_errors(metadata)
    entry, subsections, body_errors = _split_body(match.group(2))
    errors += body_errors
    if errors:
        raise FragmentError(path, errors)

    return Fragment(
        path=path,
        type=metadata["type"],
        date=date.fromisoformat(metadata["date"]),
        pr=metadata["pr"],
        liens=tuple(metadata.get("liens") or ()),
        entry=entry,
        subsections=subsections,
        routes=_cited_routes(match.group(2)),
    )


def _cited_routes(body: str) -> tuple[str, ...]:
    return tuple(sorted({route.rstrip("/") for route in _ROUTE.findall(body)}))


def _metadata_errors(metadata: dict[str, Any]) -> list[str]:
    errors = [f"champ inconnu `{key}`" for key in metadata.keys() - _FIELDS]

    if metadata.get("type") not in TYPES:
        errors.append(f"`type` doit valoir {', '.join(f'`{t}`' for t in TYPES)}")

    raw_date = metadata.get("date")
    if not isinstance(raw_date, str) or not _DATE_FORMAT.fullmatch(raw_date):
        errors.append("`date` doit être au format AAAA-MM-JJ")
    else:
        try:
            date.fromisoformat(raw_date)
        except ValueError:
            errors.append(f"`date` n'est pas une date valide : {raw_date}")

    pr = metadata.get("pr")
    if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
        errors.append("`pr` doit être le numéro de la PR")

    liens = metadata.get("liens") or []
    if not isinstance(liens, list) or not all(_is_url(lien) for lien in liens):
        errors.append("`liens` doit être une liste d'URL `http` ou `https`")

    return errors


def _is_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    url = urlparse(value)
    return url.scheme in ("http", "https") and bool(url.netloc)


def _split_body(body: str) -> tuple[str, tuple[tuple[str, str], ...], list[str]]:
    errors = []
    if re.search(r"^#{1,2} ", body, re.MULTILINE):
        errors.append("le corps n'accepte que des titres de niveau `###` ou plus")

    parts = _SUBSECTION.split(body)
    entry = parts[0].strip()
    if not entry:
        errors.append("le corps doit décrire le changement avant toute sous-section")

    subsections = []
    for title, text in zip(parts[1::2], parts[2::2], strict=True):
        if not text.strip():
            errors.append(f"la sous-section « {title.strip()} » est vide")
        subsections.append((title.strip(), text.strip()))

    return entry, tuple(subsections), errors


def load_fragments(directory: Path = FRAGMENTS_DIR) -> list[Fragment]:
    return [parse_fragment(path) for path in sorted(directory.glob("*.md"))]


def assemble(
    fragments: Iterable[Fragment], *, base_url: str = "", note: str = ""
) -> str:
    """Base URL makes the header links absolute, for a downloaded file."""
    by_date: dict[date, list[Fragment]] = {}
    for fragment in fragments:
        by_date.setdefault(fragment.date, []).append(fragment)

    sections = [HEADER.format(base=base_url).rstrip()]
    if note:
        sections.append(note)
    if not by_date:
        sections.append("Aucun changement ne correspond aux filtres.")
    for day in sorted(by_date, reverse=True):
        day_fragments = sorted(by_date[day], key=lambda f: f.sort_key)
        sections.append(f"## {day.isoformat()}")

        for type_, title in TYPES.items():
            entries = [render_entry(f) for f in day_fragments if f.type == type_]
            if entries:
                sections.append(f"### {title}")
                sections.append(_join_entries(entries))

    return "\n\n".join(sections) + "\n"


def render_entry(fragment: Fragment) -> str:
    """Keeps each subsection under its own entry, as a blockquote."""
    blocks = [_with_links(fragment)]
    # Indented, the quote belongs to the bullet. An entry of several bullets keeps
    # it below the whole list, as it applies to all of them.
    bullets = [line for line in fragment.entry.splitlines() if line.startswith("- ")]
    single_bullet = fragment.entry.startswith("- ") and len(bullets) == 1
    indent = "  " if single_bullet else ""
    for title, text in fragment.subsections:
        quote = f"**{title}**\n\n{text}"
        blocks.append(
            "\n".join(f"{indent}> {line}".rstrip() for line in quote.splitlines())
        )
    return "\n\n".join(blocks)


def _with_links(fragment: Fragment) -> str:
    links = [f"[PR #{fragment.pr}]({fragment.pr_url})"]
    for url in fragment.liens:
        reference = _GITHUB_REFERENCE.fullmatch(url)
        label = f"#{reference.group(1)}" if reference else url
        links.append(f"[{label}]({url})")
    suffix = f"({', '.join(links)})"

    last_line = fragment.entry.rsplit("\n", 1)[-1]
    if last_line.startswith(("```", "~~~")):
        return f"{fragment.entry}\n\n{suffix}"
    return f"{fragment.entry} {suffix}"


def _join_entries(entries: list[str]) -> str:
    """Keeps consecutive bullet lists tight, as a single list."""
    joined = entries[0]
    for entry in entries[1:]:
        last_line = joined.rsplit("\n", 1)[-1]
        in_list = last_line.startswith(("- ", " "))
        separator = "\n" if in_list and entry.startswith("- ") else "\n\n"
        joined += separator + entry
    return joined


def paris_today() -> date:
    return datetime.now(ZoneInfo("Europe/Paris")).date()


def check_added_fragment(
    fragment: Fragment, today: date, *, merge_queue: bool, pr: int | None
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    fix = f"lancez `{DATE_COMMAND}` pour la remplacer par {today.isoformat()}"

    if fragment.date > today:
        errors.append(f"la date {fragment.date.isoformat()} est dans le futur, {fix}")
    elif fragment.date < today - DATE_TOLERANCE:
        message = (
            f"la date {fragment.date.isoformat()} a plus de "
            f"{DATE_TOLERANCE.days} jours, {fix}"
        )
        (errors if merge_queue else warnings).append(message)

    if not merge_queue and pr is not None and fragment.pr != pr:
        errors.append(f"`pr` vaut {fragment.pr} au lieu de {pr}, le numéro de la PR")

    return errors, warnings


_markdown = MarkdownIt("commonmark", {"html": False})


def entry_html(fragment: Fragment) -> str:
    return _markdown.render(render_entry(fragment))


def ordered(fragments: Iterable[Fragment]) -> list[Fragment]:
    """Most recent first, then in the order of the assembled changelog."""
    by_type = sorted(fragments, key=lambda f: f.sort_key)
    return sorted(by_type, key=lambda f: f.date, reverse=True)


@cache
def published_fragments() -> tuple[Fragment, ...]:
    return tuple(ordered(load_fragments()))


@cache
def changelog_markdown() -> str:
    return assemble(published_fragments())


def cited_routes(fragments: Iterable[Fragment]) -> list[str]:
    return sorted({route for fragment in fragments for route in fragment.routes})


def as_json(fragment: Fragment, page_url: str) -> dict[str, Any]:
    return {
        "id": fragment.slug,
        "date": fragment.date.isoformat(),
        "type": fragment.type,
        "libelle_type": TYPE_LABELS[fragment.type],
        "routes": list(fragment.routes),
        "pr": fragment.pr,
        "pr_url": fragment.pr_url,
        "liens": list(fragment.liens),
        "url": f"{page_url}#{fragment.slug}",
        "contenu": fragment.entry,
        "sous_sections": [
            {"titre": title, "contenu": text} for title, text in fragment.subsections
        ],
    }


@dataclass(frozen=True)
class Filters:
    types: frozenset[str] = frozenset()
    route: str = ""
    since: date | None = None
    errors: tuple[str, ...] = field(default=(), compare=False)

    @classmethod
    def from_query(cls, query: QueryDict) -> "Filters":
        """Reads `type` (repeatable), `route` and `depuis`."""
        errors = []
        types = query.getlist("type")
        unknown = [t for t in types if t not in TYPES]
        if unknown:
            errors.append(
                f"`type` inconnu : {', '.join(unknown)}. Valeurs possibles : "
                f"{', '.join(TYPES)}."
            )
        route = (query.get("route") or "").strip().rstrip("/")
        since = None
        if raw_since := (query.get("depuis") or "").strip():
            try:
                since = date.fromisoformat(raw_since)
            except ValueError:
                errors.append(f"`depuis` doit être une date AAAA-MM-JJ : {raw_since}.")
        return cls(
            types=frozenset(t for t in types if t in TYPES),
            route=route,
            since=since,
            errors=tuple(errors),
        )

    @property
    def active(self) -> bool:
        return bool(self.types or self.route or self.since)

    def apply(self, fragments: Iterable[Fragment]) -> list[Fragment]:
        return [
            fragment
            for fragment in fragments
            if (not self.types or fragment.type in self.types)
            and (not self.route or self.route in fragment.routes)
            and (self.since is None or fragment.date >= self.since)
        ]

    def query_string(self) -> str:
        params: list[tuple[str, str]] = [("type", t) for t in TYPES if t in self.types]
        if self.route:
            params.append(("route", self.route))
        if self.since:
            params.append(("depuis", self.since.isoformat()))
        return urlencode(params)

    def describe(self) -> str:
        parts = []
        if self.types:
            labels = [TYPE_LABELS[t] for t in TYPES if t in self.types]
            parts.append(f"type {', '.join(labels).lower()}")
        if self.route:
            parts.append(f"route `{self.route}`")
        if self.since:
            parts.append(f"depuis le {self.since.isoformat()}")
        return f"Changements filtrés : {' ; '.join(parts)}." if parts else ""


def known_routes(
    schema_path: Path = settings.STATIC_DIR / "api" / "schema.yaml",
) -> list[re.Pattern]:
    """Routes of the public OpenAPI schema, as patterns, plus DOC_ROUTES."""
    schema = yaml.safe_load(schema_path.read_text())
    routes = [
        f"{method.upper()} {path.rstrip('/')}"
        for path, operations in schema["paths"].items()
        for method in operations
        if method in ("get", "post", "put", "patch", "delete")
    ]
    return [
        re.compile(_PATH_PARAMETER.sub("[^/]+", re.escape(route)) + r"\Z")
        for route in (*routes, *DOC_ROUTES)
    ]


def route_errors(fragment: Fragment, known: list[re.Pattern] | None) -> list[str]:
    """Without `known`, only checks that the fragment cites a route."""
    if not fragment.routes:
        return [
            (
                "le corps doit citer la ou les routes concernées, par exemple "
                "`GET /api/v1/offres`"
            )
        ]
    if known is None or fragment.type == "retire":
        return []
    return [
        f"route inconnue du schéma de l'API publique : `{route}`"
        for route in fragment.routes
        if not any(pattern.match(route) for pattern in known)
    ]


def set_date(path: Path, day: date) -> None:
    text = path.read_text()
    match = _FRONT_MATTER.match(text)
    if match is None:
        raise FragmentError(path, ["en-tête YAML absent"])
    front_matter, count = re.subn(
        r"^(date:[ \t]*)[^\s#]*",
        rf"\g<1>{day.isoformat()}",
        match.group(1),
        count=1,
        flags=re.MULTILINE,
    )
    if count == 0:
        raise FragmentError(path, ["champ `date` absent de l'en-tête"])
    path.write_text(f"---\n{front_matter}\n---\n{match.group(2)}")
