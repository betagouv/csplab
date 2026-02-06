"""Mapper for transforming Concours entities to template format."""

from domain.entities.concours import Concours
from domain.value_objects.category import Category
from domain.value_objects.verse import Verse


class ConcoursToTemplateMapper:
    """Maps Concours entities to template-compatible dictionaries."""

    @staticmethod
    def map(concours: Concours) -> dict[str, str | list[str]]:
        """Transform a Concours entity to template format.

        Args:
            concours: The Concours entity to transform

        Returns:
            Dictionary with template-compatible format
        """
        return {
            "type": "concours",
            "title": concours.corps,
            "description": concours.grade,
            "concours_type": [str(modality) for modality in concours.access_modality]
            if concours.access_modality
            else [],
            "category": ConcoursToTemplateMapper._format_category_display(
                concours.category
            ),
            "category_value": ConcoursToTemplateMapper._format_category_value(
                concours.category
            ),
            "versant": ConcoursToTemplateMapper._format_verse(Verse.FPE),
            "job_type": "",
            "url": "#",
        }

    @staticmethod
    def _format_category_display(category: Category) -> str:
        """Format category for display (e.g., 'Catégorie A').

        Args:
            category: The Category enum value

        Returns:
            Formatted category string for display
        """
        if category == Category.APLUS:
            return "Catégorie A"
        elif category == Category.HORS_CATEGORIE:
            return "Hors catégorie"
        else:
            return f"Catégorie {category.value}"

    @staticmethod
    def _format_category_value(category: Category) -> str:
        """Format category value for filtering (lowercase).

        Args:
            category: The Category enum value

        Returns:
            Lowercase category value for filtering
        """
        if category == Category.APLUS:
            return Category.A.value.lower()
        elif category == Category.HORS_CATEGORIE:
            return "hors_categorie"
        else:
            return category.value.lower()

    @staticmethod
    def _format_verse(verse: Verse) -> str:
        """Format verse value for filtering (lowercase).

        Args:
            verse: The Verse enum value
        Returns:
            Formatted verse string for display
        """
        if verse == Verse.FPE:
            return "Fonction publique d'État"
        elif verse == Verse.FPH:
            return "Fonction publique Hospitalière"
        else:
            return "Fonction publique Territoriale"
