from datetime import date
from textwrap import dedent

import pytest
from django.core.management import CommandError, call_command
from django.urls import reverse
from rest_framework import status

from presentation.api.changelog_api import (
    FragmentError,
    assemble,
    check_added_fragment,
    load_fragments,
    parse_fragment,
    set_date,
)

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

    def test_groups_subsections_after_the_types(self, tmp_path):
        fragments = [
            fragment(
                tmp_path,
                "a.md",
                type_="non_retrocompatible",
                pr=2,
                body="Cassé.\n\n### Compatibilité\n\nCompat 2.",
            ),
            fragment(
                tmp_path,
                "b.md",
                type_="ajoute",
                pr=1,
                body="Ajouté.\n\n### Compatibilité\n\nCompat 1.",
            ),
        ]

        markdown = assemble(fragments)

        assert markdown.count("### Compatibilité") == 1
        assert markdown.index("Ajouté.") < markdown.index("### Compatibilité")
        assert "### Compatibilité\n\nCompat 2.\n\nCompat 1." in markdown

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


@pytest.mark.parametrize("name", ["f.markdown", "f.MD", "f"])
def test_verifier_command_rejects_another_extension(tmp_path, monkeypatch, name):
    monkeypatch.setattr(
        "presentation.ingestion.management.commands.changelog_api.FRAGMENTS_DIR",
        tmp_path,
    )
    # GitHub annotations need a path inside the repository.
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    write_fragment(tmp_path, name, header="type: ajoute\ndate: 2026-10-27\npr: 1")

    with pytest.raises(CommandError, match="1 erreur"):
        call_command("changelog_api", "verifier")


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
