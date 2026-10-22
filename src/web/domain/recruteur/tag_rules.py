import unicodedata

from domain.recruteur.errors.tag_errors import InvalidTagName

TAG_NAME_MAX_LENGTH = 25

_FORBIDDEN_CHARACTERS = {"<", ">"}
# Emojis are "other symbols" (So) glued by joiners (Cf), variation selectors and
# enclosing keycaps (Me). Latin-1 symbols such as "°" or "©" are So but not emojis;
# skin tone modifiers are Sk but are emojis.
_FORBIDDEN_CATEGORIES = {"So", "Cc", "Cf", "Cs", "Co", "Cn", "Me"}
_LATIN_1 = range(0x00A0, 0x0100)
_VARIATION_SELECTORS = range(0xFE00, 0xFE10)
_SKIN_TONE_MODIFIERS = range(0x1F3FB, 0x1F400)


def _is_forbidden(character: str) -> bool:
    code_point = ord(character)
    if code_point in _LATIN_1:
        return False
    return (
        character in _FORBIDDEN_CHARACTERS
        or code_point in _VARIATION_SELECTORS
        or code_point in _SKIN_TONE_MODIFIERS
        or unicodedata.category(character) in _FORBIDDEN_CATEGORIES
    )


def normalize_tag_name(raw: str) -> str:
    name = " ".join(unicodedata.normalize("NFC", raw).split())
    if not name:
        raise InvalidTagName("Le libellé de l'étiquette est obligatoire")
    if len(name) > TAG_NAME_MAX_LENGTH:
        raise InvalidTagName(
            f"Le libellé de l'étiquette ne doit pas dépasser {TAG_NAME_MAX_LENGTH} "
            "caractères"
        )
    if any(_is_forbidden(character) for character in name):
        raise InvalidTagName("Les émojis et les caractères < > ne sont pas autorisés.")
    return name
