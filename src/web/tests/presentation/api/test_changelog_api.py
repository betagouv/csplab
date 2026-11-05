import xml.etree.ElementTree as ET
from datetime import date
from textwrap import dedent
from unittest.mock import patch

import pytest
import yaml
from django.conf import settings
from django.core.management import CommandError, call_command
from django.http import QueryDict
from django.urls import reverse
from rest_framework import status

from infrastructure.authentication.rate_throttle import DocumentationRateThrottle
from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel
from presentation.api.changelog_api import (
    TYPE_LABELS,
    TYPES,
    Filters,
    FragmentError,
    assemble,
    check_added_fragment,
    known_routes,
    load_fragments,
    ordered,
    page_size_error,
    parse_fragment,
    published_fragments,
    route_errors,
    set_date,
)
from presentation.api.serializers import ChangelogEntrySerializer
from presentation.api.views import ChangelogJsonView
from presentation.pages.views import _BADGES

TODAY = date(2026, 10, 27)


def write_fragment(tmp_path, name, *, header, body="Un changement."):
    path = tmp_path / name
    path.write_text(f"---\n{dedent(header).strip()}\n---\n\n{dedent(body).strip()}\n")
    return path


def fragment(tmp_path, name="f.md", *, type_="ajoute", day="2026-10-27", pr=1, **kw):
    header = f"type: {type_}\ndate: {day}\npr: {pr}\n" + kw.pop("extra", "")
    return parse_fragment(write_fragment(tmp_path, name, header=header, **kw))


class TestParseFragment:
    def test_valid_fragment(self, tmp_path):
        path = write_fragment(
            tmp_path,
            "f.md",
            header="""
                type: non_retrocompatible  # commentaire
                date: 2026-10-27
                pr: 2085
                liens:
                  - https://github.com/betagouv/csplab/issues/2072
            """,
            body="""
                Un changement.

                ### Compatibilité

                Faites autrement.
            """,
        )

        result = parse_fragment(path)

        assert result.type == "non_retrocompatible"
        assert result.date == date(2026, 10, 27)
        assert result.pr == 2085  # noqa: PLR2004
        assert result.liens == ("https://github.com/betagouv/csplab/issues/2072",)
        assert result.entry == "Un changement."
        assert result.subsections == (("Compatibilité", "Faites autrement."),)

    def test_extracts_cited_routes(self, tmp_path):
        result = fragment(
            tmp_path,
            body="""
                `GET /api/v1/offres/` et `POST /api/v1/offres/creer_modifier`, comme
                `GET /api/v1/offres`. La route /api/v1/metiers n'est pas citée.

                ### Compatibilité

                Appelez `GET /api/v1/organismes`.
            """,
        )

        assert result.routes == (
            "GET /api/v1/offres",
            "GET /api/v1/organismes",
            "POST /api/v1/offres/creer_modifier",
        )
        assert result.slug == "f"

    def test_missing_front_matter(self, tmp_path):
        path = tmp_path / "f.md"
        path.write_text("Un changement.\n")

        with pytest.raises(FragmentError, match="en-tête YAML absent"):
            parse_fragment(path)

    @pytest.mark.parametrize(
        "header, message",
        [
            ("type: autre\ndate: 2026-10-27\npr: 1", "`type` doit valoir"),
            ("type: ajoute\ndate: 2026-1-5\npr: 1", "`date` doit être au format"),
            ("type: ajoute\ndate: 2026-02-30\npr: 1", "pas une date valide"),
            ("type: ajoute\npr: 1", "`date` doit être au format"),
            ("type: ajoute\ndate: 2026-10-27\npr: '12'", "`pr` doit être"),
            ("type: ajoute\ndate: 2026-10-27", "`pr` doit être"),
            (
                "type: ajoute\ndate: 2026-10-27\npr: 1\nliens: [pas-une-url]",
                "`liens` doit être",
            ),
            ("type: ajoute\ndate: 2026-10-27\npr: 1\nauteur: x", "champ inconnu"),
        ],
    )
    def test_invalid_header(self, tmp_path, header, message):
        path = write_fragment(tmp_path, "f.md", header=header)

        with pytest.raises(FragmentError, match=message):
            parse_fragment(path)

    @pytest.mark.parametrize(
        "body, message",
        [
            ("### Compatibilité\n\nTexte.", "décrire le changement"),
            ("Un changement.\n\n## Titre", "titres de niveau `###`"),
            ("Un changement.\n\n### Compatibilité\n", "est vide"),
        ],
    )
    def test_invalid_body(self, tmp_path, body, message):
        path = write_fragment(
            tmp_path, "f.md", header="type: ajoute\ndate: 2026-10-27\npr: 1", body=body
        )

        with pytest.raises(FragmentError, match=message):
            parse_fragment(path)


class TestAssemble:
    def test_orders_by_date_then_type_then_pr(self, tmp_path):
        fragments = [
            fragment(tmp_path, "a.md", type_="corrige", pr=3, body="Corrigé 3."),
            fragment(tmp_path, "b.md", type_="ajoute", pr=5, body="Ajouté 5."),
            fragment(tmp_path, "c.md", type_="ajoute", pr=4, body="Ajouté 4."),
            fragment(tmp_path, "d.md", day="2026-10-20", pr=1, body="Ancien."),
            fragment(tmp_path, "e.md", type_="non_retrocompatible", body="Cassé."),
        ]

        markdown = assemble(fragments)

        positions = [
            markdown.index(text)
            for text in (
                "## 2026-10-27",
                "### ⚠️ Changements non rétrocompatibles",
                "Cassé.",
                "### Ajouté",
                "Ajouté 4.",
                "Ajouté 5.",
                "### Corrigé",
                "Corrigé 3.",
                "## 2026-10-20",
                "Ancien.",
            )
        ]
        assert positions == sorted(positions)
        assert markdown.startswith("Ce changelog liste les changements")

    def test_appends_links_to_the_entry(self, tmp_path):
        result = fragment(
            tmp_path,
            pr=2085,
            extra=(
                "liens:\n"
                "  - https://github.com/betagouv/csplab/issues/2072\n"
                "  - https://example.com/doc\n"
            ),
        )

        assert (
            "Un changement. ([PR #2085](https://github.com/betagouv/csplab/pull/2085), "
            "[#2072](https://github.com/betagouv/csplab/issues/2072), "
            "[https://example.com/doc](https://example.com/doc))"
        ) in assemble([result])

    def test_renders_subsections_under_their_entry(self, tmp_path):
        fragments = [
            fragment(
                tmp_path,
                "a.md",
                type_="non_retrocompatible",
                pr=2,
                body="Cassé 2.\n\n### Compatibilité\n\nCompat 2.\n\n- Point.",
            ),
            fragment(
                tmp_path,
                "b.md",
                type_="non_retrocompatible",
                pr=3,
                body="Cassé 3.\n\n### Compatibilité\n\nCompat 3.",
            ),
        ]

        markdown = assemble(fragments)

        assert "### Compatibilité" not in markdown
        assert (
            "Cassé 2. ([PR #2](https://github.com/betagouv/csplab/pull/2))\n\n"
            "> **Compatibilité**\n>\n> Compat 2.\n>\n> - Point.\n\n"
            "Cassé 3. ([PR #3](https://github.com/betagouv/csplab/pull/3))\n\n"
            "> **Compatibilité**\n>\n> Compat 3."
        ) in markdown

    def test_indents_subsections_of_a_bullet_entry(self, tmp_path):
        result = fragment(tmp_path, body="- Modifié.\n\n### Compatibilité\n\nCompat.")

        assert "pull/1))\n\n  > **Compatibilité**\n  >\n  > Compat." in assemble(
            [result]
        )

    def test_keeps_subsections_of_several_bullets_below_the_list(self, tmp_path):
        result = fragment(
            tmp_path, body="- Premier.\n- Second.\n\n### Compatibilité\n\nCompat."
        )

        assert "pull/1))\n\n> **Compatibilité**\n>\n> Compat." in assemble([result])

    def test_keeps_consecutive_bullet_lists_tight(self, tmp_path):
        fragments = [
            fragment(tmp_path, "a.md", pr=1, body="- Premier."),
            fragment(tmp_path, "b.md", pr=2, body="- Second."),
            fragment(tmp_path, "c.md", pr=3, body="Un paragraphe."),
        ]

        markdown = assemble(fragments)

        assert "- Premier. ([PR #1]" in markdown
        assert "pull/1))\n- Second. ([PR #2]" in markdown
        assert "pull/2))\n\nUn paragraphe." in markdown

    def test_published_fragments_are_valid(self):
        assert assemble(load_fragments()).count("## 2026-") >= 1

    def test_makes_header_links_absolute(self, tmp_path):
        markdown = assemble([fragment(tmp_path)], base_url="https://csplab.fr")

        assert "[guide de l'API](https://csplab.fr/pages/guide_api)" in markdown
        assert "[JSON](https://csplab.fr/api/changelog.json)" in markdown

    def test_adds_the_note_and_says_when_nothing_matches(self):
        markdown = assemble([], note="Changements filtrés : type ajouté.")

        assert "Changements filtrés : type ajouté.\n\nAucun changement" in markdown


def test_ordered_by_date_then_type_then_pr(tmp_path):
    old = fragment(tmp_path, "a.md", day="2026-10-20")
    added = fragment(tmp_path, "b.md", pr=2)
    broken = fragment(tmp_path, "c.md", type_="non_retrocompatible", pr=3)

    assert ordered([old, added, broken]) == [broken, added, old]


def test_changelog_entry_serializer(tmp_path):
    result = fragment(
        tmp_path,
        "2219-null.md",
        pr=2236,
        extra="liens:\n  - https://github.com/betagouv/csplab/issues/2219\n",
        body="`GET /api/v1/offres` change.\n\n### Compatibilité\n\nLisez `null`.",
    )

    context = {"page_url": "https://csplab.fr/pages/changelog_api"}
    assert ChangelogEntrySerializer(result, context=context).data == {
        "id": "2219-null",
        "date": "2026-10-27",
        "type": "ajoute",
        "libelle_type": "Ajouté",
        "routes": ["GET /api/v1/offres"],
        "pr": 2236,
        "pr_url": "https://github.com/betagouv/csplab/pull/2236",
        "liens": ["https://github.com/betagouv/csplab/issues/2219"],
        "url": "https://csplab.fr/pages/changelog_api#2219-null",
        "contenu": "`GET /api/v1/offres` change.",
        "sous_sections": [{"titre": "Compatibilité", "contenu": "Lisez `null`."}],
    }


def test_every_type_has_a_title_a_label_and_a_badge():
    assert set(TYPES) == set(TYPE_LABELS) == set(_BADGES)


class TestFilters:
    ROUTES = ("GET /api/v1/metiers", "GET /api/v1/offres")

    def test_reads_the_query(self):
        filters = Filters.from_query(
            QueryDict(
                "type=ajoute&type=non_retrocompatible"
                "&route=GET+/api/v1/offres/&depuis=2026-10-15"
            ),
            self.ROUTES,
        )

        assert filters == Filters(
            types=frozenset({"ajoute", "non_retrocompatible"}),
            route="GET /api/v1/offres",
            since=date(2026, 10, 15),
        )
        assert filters.errors == ()
        assert filters.active
        assert filters.query_string() == (
            "type=non_retrocompatible&type=ajoute"
            "&route=GET+%2Fapi%2Fv1%2Foffres&depuis=2026-10-15"
        )
        assert filters.describe() == (
            "Changements filtrés : type non rétrocompatible, ajouté ; "
            "route `GET /api/v1/offres` ; depuis le 2026-10-15."
        )

    def test_reports_invalid_values_without_quoting_them(self):
        filters = Filters.from_query(
            QueryDict("type=autre&route=GET+/api/v1/injecte&depuis=15/10/2026"),
            self.ROUTES,
        )

        assert filters == Filters()
        assert not filters.active
        assert filters.describe() == ""
        assert filters.errors == (
            (
                "`type` : valeur inconnue. Valeurs possibles : non_retrocompatible, "
                "ajoute, modifie, corrige, retire."
            ),
            (
                "`route` n'est citée par aucun changement. Valeurs possibles : "
                "GET /api/v1/metiers, GET /api/v1/offres."
            ),
            "`depuis` doit être une date AAAA-MM-JJ.",
        )

    def test_keeps_the_valid_types_of_a_partially_invalid_query(self):
        filters = Filters.from_query(QueryDict("type=ajoute&type=autre"), self.ROUTES)

        assert filters == Filters(types=frozenset({"ajoute"}))
        assert filters.errors == (
            (
                "`type` : valeur inconnue. Valeurs possibles : non_retrocompatible, "
                "ajoute, modifie, corrige, retire."
            ),
        )

    def test_apply(self, tmp_path):
        offres = fragment(tmp_path, "a.md", body="`GET /api/v1/offres`.")
        metiers = fragment(
            tmp_path, "b.md", type_="corrige", body="`GET /api/v1/metiers`."
        )
        old = fragment(tmp_path, "c.md", day="2026-10-01", body="`GET /api/v1/offres`.")
        fragments = [offres, metiers, old]

        assert Filters().apply(fragments) == fragments
        assert Filters(types=frozenset({"corrige"})).apply(fragments) == [metiers]
        assert Filters(route="GET /api/v1/offres").apply(fragments) == [offres, old]
        assert Filters(since=date(2026, 10, 2)).apply(fragments) == [offres, metiers]


class TestRouteErrors:
    def test_requires_a_route(self, tmp_path):
        assert route_errors(fragment(tmp_path), known=None) == [
            (
                "le corps doit citer la ou les routes concernées, par exemple "
                "`GET /api/v1/offres`"
            )
        ]

    def test_rejects_a_route_absent_from_the_schema(self, tmp_path):
        result = fragment(
            tmp_path,
            body=(
                "`GET /api/v1/offres/sources/42`, `GET /api/fake-ts/referentials/x`, "
                "`GET /api/changelog.md` et `POST /api/v1/offre`."
            ),
        )

        assert route_errors(result, known_routes()) == [
            "route inconnue du schéma de l'API publique : `POST /api/v1/offre`"
        ]

    def test_accepts_a_removed_route(self, tmp_path):
        result = fragment(tmp_path, type_="retire", body="`GET /api/v1/disparue`.")

        assert route_errors(result, known_routes()) == []


class TestCheckAddedFragment:
    @pytest.mark.parametrize("merge_queue", [True, False])
    def test_rejects_a_future_date(self, tmp_path, merge_queue):
        errors, _ = check_added_fragment(
            fragment(tmp_path, day="2026-10-28"), TODAY, merge_queue=merge_queue, pr=1
        )

        assert errors == [
            (
                "la date 2026-10-28 est dans le futur, lancez "
                "`mise run web:changelog-api:dater` pour la remplacer par 2026-10-27"
            )
        ]

    @pytest.mark.parametrize("day", ["2026-10-24", "2026-10-27"])
    def test_accepts_a_date_within_tolerance(self, tmp_path, day):
        assert check_added_fragment(
            fragment(tmp_path, day=day), TODAY, merge_queue=True, pr=None
        ) == ([], [])

    def test_old_date_fails_the_merge_queue(self, tmp_path):
        errors, warnings = check_added_fragment(
            fragment(tmp_path, day="2026-10-23"), TODAY, merge_queue=True, pr=None
        )

        assert len(errors) == 1
        assert "plus de 3 jours" in errors[0]
        assert warnings == []

    def test_old_date_only_warns_on_the_pull_request(self, tmp_path):
        errors, warnings = check_added_fragment(
            fragment(tmp_path, day="2026-10-23"), TODAY, merge_queue=False, pr=1
        )

        assert errors == []
        assert len(warnings) == 1

    def test_rejects_another_pr_number(self, tmp_path):
        errors, _ = check_added_fragment(
            fragment(tmp_path, pr=12), TODAY, merge_queue=False, pr=13
        )

        assert errors == ["`pr` vaut 12 au lieu de 13, le numéro de la PR"]


def test_set_date_only_changes_the_date(tmp_path):
    path = write_fragment(
        tmp_path,
        "f.md",
        header="type: ajoute\ndate: 2026-10-01  # date de merge\npr: 1",
        body="date: 2026-10-01 dans le corps.",
    )

    set_date(path, TODAY)

    assert path.read_text() == (
        "---\ntype: ajoute\ndate: 2026-10-27  # date de merge\npr: 1\n---\n\n"
        "date: 2026-10-01 dans le corps.\n"
    )


def test_verifier_command_accepts_published_fragments(capsys):
    call_command("changelog_api", "verifier")

    assert "fragment(s) valide(s)" in capsys.readouterr().out


def test_verifier_command_fails_when_the_page_grows_too_long(
    tmp_path, monkeypatch, capsys
):
    module = "presentation.ingestion.management.commands.changelog_api"
    monkeypatch.setattr(f"{module}.FRAGMENTS_DIR", tmp_path)
    monkeypatch.setattr(f"{module}.load_fragments", lambda: [None] * 300)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)

    with pytest.raises(CommandError, match="1 erreur"):
        call_command("changelog_api", "verifier")
    assert "300 changements publiés (seuil : 300)" in capsys.readouterr().out


def test_page_size_error():
    assert page_size_error(299) is None
    assert page_size_error(300)


@pytest.mark.parametrize("name", ["f.markdown", "f.MD", "f"])
def test_verifier_command_rejects_another_extension(tmp_path, monkeypatch, name):
    monkeypatch.setattr(
        "presentation.ingestion.management.commands.changelog_api.FRAGMENTS_DIR",
        tmp_path,
    )
    # GitHub annotations need a path inside the repository.
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    write_fragment(
        tmp_path,
        name,
        header="type: ajoute\ndate: 2026-10-27\npr: 1",
        body="`GET /api/v1/offres`.",
    )

    with pytest.raises(CommandError, match="1 erreur"):
        call_command("changelog_api", "verifier")


def test_verifier_command_rejects_a_fragment_without_route(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "presentation.ingestion.management.commands.changelog_api.FRAGMENTS_DIR",
        tmp_path,
    )
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    write_fragment(tmp_path, "f.md", header="type: ajoute\ndate: 2026-10-27\npr: 1")

    with pytest.raises(CommandError, match="1 erreur"):
        call_command("changelog_api", "verifier")


class TestVerifierCommandOnAddedFragments:
    @pytest.fixture
    def added(self, tmp_path, monkeypatch):
        module = "presentation.ingestion.management.commands.changelog_api"
        monkeypatch.setattr(f"{module}.FRAGMENTS_DIR", tmp_path)
        monkeypatch.setattr(f"{module}.paris_today", lambda: TODAY)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)

        def add(type_, body):
            path = write_fragment(
                tmp_path,
                "f.md",
                header=f"type: {type_}\ndate: 2026-10-27\npr: 1",
                body=body,
            )
            monkeypatch.setattr(f"{module}._added_fragments", lambda base: [path])

        return add

    def test_rejects_a_route_absent_from_the_schema(self, added, capsys):
        added("ajoute", "`POST /api/v1/offre`.")

        with pytest.raises(CommandError, match="1 erreur"):
            call_command("changelog_api", "verifier", "--base", "main", "--pr", "1")
        assert "route inconnue" in capsys.readouterr().out

    def test_accepts_a_removed_route(self, added):
        added("retire", "`GET /api/v1/disparue`.")

        call_command("changelog_api", "verifier", "--base", "main", "--pr", "1")

    def test_exempte_skips_the_schema_check(self, added):
        added("ajoute", "`POST /api/v1/offre`.")

        call_command(
            "changelog_api", "verifier", "--base", "main", "--pr", "1", "--exempte"
        )


class TestPublicSchemaView:
    def test_serves_the_schema_with_the_changelog(self, db, client):
        response = client.get(reverse("api:public_schema"))

        assert response.status_code == status.HTTP_200_OK
        changelog = next(t for t in response.json()["tags"] if t["name"] == "changelog")
        assert changelog["x-displayName"] == "Changelog"
        assert changelog["description"].startswith("Ce changelog liste")
        assert (
            "([PR #2084](https://github.com/betagouv/csplab/pull/2084)"
            in (changelog["description"])
        )


class TestChangelogMarkdownView:
    def test_serves_the_changelog_with_absolute_links(self, db, client):
        response = client.get(reverse("api:changelog_markdown"))

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "text/markdown; charset=utf-8"
        content = response.content.decode()
        assert content.startswith("Ce changelog liste")
        assert "(http://testserver/pages/guide_api)" in content
        assert "[PR #2084](https://github.com/betagouv/csplab/pull/2084)" in content

    def test_filters(self, db, client):
        response = client.get(
            reverse("api:changelog_markdown"),
            {"type": "retire", "route": "POST /api/v1/offres/creer_modifier"},
        )

        content = response.content.decode()
        assert "Changements filtrés : type retiré ; route" in content
        assert "### Retiré" in content
        assert "### Ajouté" not in content

    def test_rejects_an_invalid_filter(self, db, client):
        response = client.get(reverse("api:changelog_markdown"), {"depuis": "hier"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "`depuis` doit être une date" in response.content.decode()


class TestChangelogJsonView:
    def test_serves_one_entry_per_fragment(self, db, client):
        response = client.get(reverse("api:changelog_json"))

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["nombre"] == len(published_fragments())
        entry = next(e for e in body["entrees"] if e["pr"] == 2084)  # noqa: PLR2004
        assert entry["url"].startswith("http://testserver/pages/changelog_api#2084-")
        assert entry["routes"]

    def test_filters_by_date(self, db, client):
        response = client.get(reverse("api:changelog_json"), {"depuis": "2026-11-01"})

        dates = [e["date"] for e in response.json()["entrees"]]
        assert dates
        assert min(dates) >= "2026-11-01"
        assert dates == sorted(dates, reverse=True)

    def test_rejects_an_invalid_filter(self, db, client):
        response = client.get(reverse("api:changelog_json"), {"type": "autre"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["erreurs"][0].startswith("`type` : valeur inconnue")


class TestChangelogFeed:
    ATOM = "{http://www.w3.org/2005/Atom}"

    def test_serves_an_atom_feed(self, db, client):
        response = client.get(reverse("api:changelog_atom"), {"type": "retire"})

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"].startswith("application/atom+xml")
        feed = ET.fromstring(response.content)  # noqa: S314
        entries = feed.findall(f"{self.ATOM}entry")
        expected = [f for f in published_fragments() if f.type == "retire"]
        assert len(entries) == len(expected)
        link = entries[0].find(f"{self.ATOM}link").get("href")
        assert link == f"http://testserver/pages/changelog_api#{expected[0].slug}"
        assert entries[0].find(f"{self.ATOM}title").text.startswith("Retiré : ")
        entry_id = entries[0].find(f"{self.ATOM}id").text
        assert entry_id == f"tag:csplab.beta.gouv.fr:changelog-api:{expected[0].slug}"

    def test_rejects_an_invalid_filter(self, db, client):
        response = client.get(reverse("api:changelog_atom"), {"depuis": "hier"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "`depuis` doit être une date" in response.content.decode()


def test_guide_markdown_view(db, client):
    response = client.get(reverse("api:guide_markdown"))

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Type"] == "text/markdown; charset=utf-8"
    assert response.content.decode().startswith("# Guide de l'API CSPLab")


@pytest.mark.parametrize(
    "name", ["api:changelog_markdown", "api:changelog_json", "api:changelog_atom"]
)
def test_rejects_an_unknown_route_without_quoting_it(db, client, name):
    response = client.get(reverse(name), {"route": "GET /api/v1/[injecté](x)"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.content.decode()
    assert "`route` n'est citée par aucun changement" in content
    assert "injecté" not in content


class TestDocumentationRoutes:
    ROUTES = (
        "api:changelog_markdown",
        "api:changelog_json",
        "api:changelog_atom",
        "api:guide_markdown",
    )

    @pytest.mark.parametrize("name", ROUTES)
    @pytest.mark.parametrize(
        "authorization", ["", "Bearer jeton-invalide", "Api-Key cle-invalide"]
    )
    def test_are_public_and_limited_to_60_calls_per_minute(
        self, db, client, name, authorization
    ):
        response = client.get(reverse(name), HTTP_AUTHORIZATION=authorization)

        assert response.status_code == status.HTTP_200_OK
        assert response["X-RateLimit-Limit"] == "60"

    @pytest.mark.parametrize(
        ("name", "accept", "content_type"),
        [
            ("api:changelog_markdown", "text/markdown", "text/markdown"),
            ("api:changelog_json", "application/json", "application/json"),
            ("api:changelog_atom", "application/atom+xml", "application/atom+xml"),
            ("api:changelog_markdown", "text/html", "text/markdown"),
            ("api:changelog_atom", "application/json", "application/atom+xml"),
        ],
    )
    def test_ignore_the_accept_header(self, db, client, name, accept, content_type):
        response = client.get(reverse(name), HTTP_ACCEPT=accept)

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"].startswith(content_type)

    @pytest.mark.parametrize("name", ROUTES)
    def test_are_not_logged_in_api_logs(self, db, client, name):
        client.get(reverse(name))
        client.get(reverse(name), {"depuis": "hier"})

        assert not ApiLogModel.objects.exists()

    def test_limits_a_caller_sending_a_valid_jwt(self, db, jwt_client):
        response = jwt_client.get(reverse("api:changelog_json"))

        assert response.status_code == status.HTTP_200_OK
        assert response["X-RateLimit-Limit"] == "60"

    @pytest.mark.parametrize("authorization", ["", "Bearer jeton-invalide"])
    @patch.object(
        DocumentationRateThrottle, "THROTTLE_RATES", {"documentation": "2/minute"}
    )
    def test_returns_429_beyond_the_limit(self, db, client, authorization):
        url = reverse("api:changelog_markdown")
        statuses = [
            client.get(url, HTTP_AUTHORIZATION=authorization).status_code
            for _ in range(3)
        ]

        assert statuses == [
            status.HTTP_200_OK,
            status.HTTP_200_OK,
            status.HTTP_429_TOO_MANY_REQUESTS,
        ]

    def test_rate_is_60_per_minute(self):
        throttle = ChangelogJsonView.throttle_classes[0]()

        assert throttle.parse_rate(throttle.get_rate()) == (60, 60)

    @pytest.mark.parametrize("name", ROUTES)
    def test_are_documented_in_the_public_schema(self, name):
        schema = yaml.safe_load(
            (settings.STATIC_DIR / "api" / "schema.yaml").read_text()
        )

        assert schema["paths"][reverse(name)]["get"]["tags"] == ["documentation"]
