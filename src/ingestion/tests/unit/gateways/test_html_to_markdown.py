import pytest

from infrastructure.gateways.html_to_markdown import html_to_markdown


def test_html_to_markdown_keeps_bold_and_lists():
    html = (
        "<p><strong>Activités principales :</strong></p>"
        "<ul><li>adaptation de contenus</li>"
        "<li>Création de pages web/mise en ligne</li></ul>"
    )

    assert html_to_markdown(html) == (
        "**Activités principales :**\n\n"
        "- adaptation de contenus\n"
        "- Création de pages web/mise en ligne"
    )


def test_html_to_markdown_keeps_italic_and_headings():
    html = "<h3>Missions</h3><p><em>Poste vacant</em></p>"

    assert html_to_markdown(html) == "### Missions\n\n*Poste vacant*"


def test_html_to_markdown_drops_inline_styles_classes_and_spans():
    html = (
        '<p style="margin: 0"><span class="ql-cursor" style="color: red">'
        'Qualités</span>&#160;: <span data-list-item-id="1">rigueur</span></p>'
    )

    assert html_to_markdown(html) == "Qualités\xa0: rigueur"


def test_html_to_markdown_converts_underline_to_bold():
    assert html_to_markdown("<p><u>Missions :</u> suivi</p>") == "**Missions :** suivi"


@pytest.mark.parametrize(
    "html",
    [
        "<p><strong><u>Missions :</u></strong></p>",
        "<p><u><strong>Missions :</strong></u></p>",
        "<p><b><u>Missions :</u></b></p>",
    ],
)
def test_html_to_markdown_does_not_double_bold_underlined_text(html):
    assert html_to_markdown(html) == "**Missions :**"


def test_html_to_markdown_keeps_line_breaks():
    assert html_to_markdown("<p>Ligne 1<br>Ligne 2</p>") == "Ligne 1\\\nLigne 2"


@pytest.mark.parametrize(
    "html",
    [
        "<p>Ligne 1<br></p><p>Ligne 2</p>",
        "<p>Ligne 1</p><p><br>Ligne 2</p>",
        "<p>Ligne 1<br><br></p><p><br></p><p>Ligne 2<br></p>",
    ],
)
def test_html_to_markdown_drops_line_breaks_at_block_edges(html):
    assert html_to_markdown(html) == "Ligne 1\n\nLigne 2"


def test_html_to_markdown_drops_images():
    html = '<p>Avant</p><img src="https://menjs.file.force.com/logo.png"><p>Après</p>'

    assert html_to_markdown(html) == "Avant\n\nAprès"


def test_html_to_markdown_flattens_tables():
    html = (
        "<table><tr><th>Lieu</th><th>Quotité</th></tr>"
        "<tr><td>Paris</td><td>100 %</td></tr></table>"
    )

    assert html_to_markdown(html) == "Lieu Quotité\nParis 100 %"


def test_html_to_markdown_drops_superscript_markup():
    assert html_to_markdown("<p>1<sup>er</sup> poste</p>") == "1er poste"


@pytest.mark.parametrize("html", ["", "<p> </p>", "<p>&nbsp;</p>", "<p><br></p>"])
def test_html_to_markdown_returns_empty_string_for_blank_html(html):
    assert html_to_markdown(html) == ""


def test_html_to_markdown_collapses_empty_paragraphs():
    html = "<p>Un</p><p>&nbsp;</p><p> </p><p>Deux</p>"

    assert html_to_markdown(html) == "Un\n\nDeux"


@pytest.mark.parametrize(
    "href",
    [
        "https://www.education.gouv.fr/concours",
        "http://www.ac-bordeaux.fr",
        "mailto:recrutement@ac-dijon.fr",
        "http://cisirh.monportail.alize/fiche",
        "https://ulysse.dgfip/page",
    ],
)
def test_html_to_markdown_keeps_valid_links(href):
    html = f'<p>Voir <a href="{href}" target="_blank" title="t">la fiche</a></p>'

    assert html_to_markdown(html) == f"Voir [la fiche]({href})"


def test_html_to_markdown_cuts_href_at_first_whitespace():
    html = (
        '<a href="https://meteofrance.com/carte-didentite-de-meteo-france  '
        'Pourquoi nous rejoindre">Météo-France</a>'
    )

    assert html_to_markdown(html) == (
        "[Météo-France](https://meteofrance.com/carte-didentite-de-meteo-france)"
    )


@pytest.mark.parametrize(
    "href",
    [
        "javascript:alert(1)",
        "JavaScript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "vbscript:msgbox(1)",
        "about:blank",
        "",
        "modernisation.gouv.fr",
        "recrutement@ac-dijon.fr",
        "(https://www.ac-dijon.fr)",
        "https://",
        "mailto:",
    ],
)
def test_html_to_markdown_turns_invalid_links_into_text(href):
    html = f'<p>Voir <a href="{href}">la fiche</a></p>'

    assert html_to_markdown(html) == "Voir la fiche"


def test_html_to_markdown_turns_link_without_href_into_text():
    assert html_to_markdown("<p>Voir <a>la fiche</a></p>") == "Voir la fiche"


def test_html_to_markdown_encodes_characters_closing_link_destination():
    html = '<a href="https://fr.wikipedia.org/wiki/Paris_(France)">Paris</a>'

    assert html_to_markdown(html) == (
        "[Paris](https://fr.wikipedia.org/wiki/Paris_%28France%29)"
    )


def test_html_to_markdown_drops_script_tags():
    html = "<p>Texte</p><script>alert(1)</script>"

    assert html_to_markdown(html) == "Texte"


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        (
            "<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>",
            "&lt;script>alert(1)&lt;/script>",
        ),
        (
            "<p>&lt;img src=x onerror=alert(1)&gt;</p>",
            "&lt;img src=x onerror=alert(1)>",
        ),
        ("<p><code>&lt;b&gt;</code></p>", "`&lt;b>`"),
        (
            '<a href="https://a.fr">&lt;b&gt;lien&lt;/b&gt;</a>',
            "[&lt;b>lien&lt;/b>](https://a.fr)",
        ),
    ],
)
def test_html_to_markdown_never_outputs_html_tags(html, expected):
    assert html_to_markdown(html) == expected


def test_html_to_markdown_keeps_comparison_signs_readable():
    assert html_to_markdown("<p>Indice &lt; 400 et &gt; 300</p>") == (
        "Indice &lt; 400 et > 300"
    )


def test_html_to_markdown_writes_link_whose_label_is_its_url_explicitly():
    html = '<a href="https://www.ac-dijon.fr">https://www.ac-dijon.fr</a>'

    assert html_to_markdown(html) == (
        "[https://www.ac-dijon.fr](https://www.ac-dijon.fr)"
    )
