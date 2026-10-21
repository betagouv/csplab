import pytest
from django.utils.safestring import SafeString

from presentation.commons.markdown import (
    forbidden_markdown,
    render_markdown_without_headings,
)
from presentation.commons.markdown import render_markdown as _render_markdown


def render_markdown(text):
    return _render_markdown(text, top_heading_level=3)


def test_returns_safe_html():
    assert isinstance(render_markdown("texte"), SafeString)


@pytest.mark.parametrize("text", [None, ""])
def test_empty_text_renders_nothing(text):
    assert render_markdown(text) == ""


def test_renders_bold_and_lists():
    html = render_markdown("**Activités :**\n\n- adapter\n- créer")

    assert html == (
        "<p><strong>Activités :</strong></p>\n<ul>\n<li>adapter</li>\n"
        "<li>créer</li>\n</ul>"
    )


def test_keeps_numbered_list_start():
    assert '<ol start="3">' in render_markdown("3. trois\n4. quatre")


@pytest.mark.parametrize("text", ["Ligne 1\nLigne 2", "Ligne 1\\\nLigne 2"])
def test_keeps_single_line_breaks_of_plain_text(text):
    assert render_markdown(text) == "<p>Ligne 1<br>\nLigne 2</p>"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("# Titre\n\n## Sous-titre", "<h3>Titre</h3>\n<h4>Sous-titre</h4>"),
        ("### Titre\n\n#### Sous-titre", "<h3>Titre</h3>\n<h4>Sous-titre</h4>"),
        ("## Titre\n\n###### Détail", "<h3>Titre</h3>\n<h6>Détail</h6>"),
    ],
)
def test_headings_start_at_the_given_level_and_keep_their_hierarchy(text, expected):
    assert render_markdown(text) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("# Titre", "<p><strong>Titre</strong></p>"),
        (
            "## Titre *accentué*\n\ntexte",
            "<p><strong>Titre <em>accentué</em></strong></p>\n<p>texte</p>",
        ),
        ("Titre\n=====", "<p><strong>Titre</strong></p>"),
        ("#", "<p><strong></strong></p>"),
    ],
)
def test_without_headings_renders_headings_as_bold_paragraphs(text, expected):
    assert render_markdown_without_headings(text) == expected


def test_without_headings_keeps_the_rest_of_the_rendering():
    text = "**gras**\n\n- un\n\n<script>alert(1)</script>"

    assert render_markdown_without_headings(text) == render_markdown(text)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.education.gouv.fr",
        "http://cisirh.monportail.alize/page",
        "mailto:rh@exemple.gouv.fr",
    ],
)
def test_links_open_in_a_new_tab(url):
    html = render_markdown(f"[libellé]({url})")

    assert html == (
        f'<p><a href="{url}" target="_blank" rel="noopener noreferrer">libellé</a></p>'
    )


@pytest.mark.parametrize(
    "text",
    [
        "[clic](javascript:alert(1))",
        "[clic](JAVASCRIPT:alert(1))",
        "[clic](vbscript:msgbox(1))",
        "[clic](data:text/html;base64,PHNjcmlwdD4=)",
        "[clic](file:///etc/passwd)",
        "[clic](/admin)",
        "<javascript:alert(1)>",
    ],
)
def test_unsafe_or_relative_links_stay_text(text):
    assert "<a" not in render_markdown(text)


@pytest.mark.parametrize(
    "text",
    [
        "<script>alert(1)</script>",
        "\\<script\\>alert(1)\\</script\\>",
        '<img src="x" onerror="alert(1)">',
    ],
)
def test_html_is_escaped(text):
    html = render_markdown(text)

    assert "<script" not in html
    assert "<img" not in html
    assert "&lt;" in html


def test_images_are_replaced_by_their_alt_text():
    html = render_markdown("![Logo <b>RH</b>](https://evil.example/x.png)")

    assert html == "<p>Logo &lt;b&gt;RH&lt;/b&gt;</p>"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("> citation", "<p>&gt; citation</p>"),
        ("    indenté", "<p>indenté</p>"),
        ("```\nbloc\n```", "<p>```<br>\nbloc<br>\n```</p>"),
        ("`code`", "<p>`code`</p>"),
    ],
)
def test_blockquotes_and_code_stay_text(text, expected):
    assert render_markdown(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "Salaire < 2000 € et > 1500 €",
        "\\<script\\>",
        "[Site](https://exemple.gouv.fr) et [RH](mailto:rh@exemple.gouv.fr)",
        "<https://exemple.gouv.fr>",
        "<rh@exemple.gouv.fr>",
        "[Intranet](http://cisirh.monportail.alize/page)",
    ],
)
def test_accepts_plain_text_escaped_html_and_allowed_links(text):
    assert forbidden_markdown(text) == []


@pytest.mark.parametrize(
    "text,excerpt",
    [
        ("<b>gras", "<b>"),
        ("<!-- commentaire -->", "<!-- commentaire -->"),
        ("> <i>citation", "<i>"),
        ("`<u>`", "<u>"),
        ("<div>" + "a" * 60, "<div>" + "a" * 45 + "…"),
    ],
)
def test_rejects_html(text, excerpt):
    assert forbidden_markdown(text) == [
        (
            f"Les balises HTML ne sont pas acceptées ({excerpt}) : utilisez la "
            "syntaxe Markdown, ou écrivez \\< pour afficher le caractère <."
        )
    ]


@pytest.mark.parametrize(
    "text,url",
    [
        ("[x](javascript:alert(1))", "javascript:alert(1)"),
        ("<javascript:alert(1)>", "javascript:alert(1)"),
        ("[x](/admin)", "/admin"),
        ("[x]()", ""),
        ("![x](data:image/png;base64,AA)", "data:image/png;base64,AA"),
        ("[x][r]\n\n[r]: vbscript:msgbox(1)", "vbscript:msgbox(1)"),
    ],
)
def test_rejects_links_other_than_http_https_and_mailto(text, url):
    message = f"Lien non autorisé ({url}) : seuls les liens http, https et mailto"
    assert forbidden_markdown(text) == [f"{message} sont acceptés."]
