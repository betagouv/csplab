import pytest

from domain.recruteur.errors.tag_errors import InvalidTagName
from domain.recruteur.tag_rules import normalize_tag_name


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  Expert  ", "Expert"),
        ("Très   bon\tprofil", "Très bon profil"),
        ("Très bon\nprofil", "Très bon profil"),
        ("Très bon\r\nprofil", "Très bon profil"),
        ("À RAPPELER", "À RAPPELER"),
        ("Bac+5, (urgent) !?", "Bac+5, (urgent) !?"),
        ("Cat. A – 2026", "Cat. A – 2026"),
        ("Vague n° 2", "Vague n° 2"),
    ],
)
def test_normalizes_spaces_and_keeps_case_accents_and_punctuation(
    raw: str, expected: str
) -> None:
    assert normalize_tag_name(raw) == expected


def test_accepts_25_characters() -> None:
    assert normalize_tag_name("a" * 25) == "a" * 25


def test_counts_length_after_normalization() -> None:
    assert normalize_tag_name("  " + "a" * 25 + "  ") == "a" * 25


def test_counts_a_decomposed_accent_as_one_character() -> None:
    assert normalize_tag_name("e\u0301" * 25) == "\u00e9" * 25


def test_rejects_26_characters() -> None:
    with pytest.raises(InvalidTagName):
        normalize_tag_name("a" * 26)


@pytest.mark.parametrize("raw", ["", "   ", "\n\t "])
def test_rejects_empty_name(raw: str) -> None:
    with pytest.raises(InvalidTagName):
        normalize_tag_name(raw)


@pytest.mark.parametrize(
    "raw",
    [
        "<b>Expert</b>",
        "a > b",
        "Top 😀",
        "Cœur ❤️",
        "Équipe 👩‍💻",
        "Clé 1️⃣",
        "France 🇫🇷",
        "Teinte \U0001f3fb",
    ],
)
def test_rejects_angle_brackets_and_emojis(raw: str) -> None:
    with pytest.raises(InvalidTagName):
        normalize_tag_name(raw)
