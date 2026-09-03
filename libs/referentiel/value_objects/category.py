from django.db.models import TextChoices


class Category(TextChoices):
    APLUS = "APLUS", "Catégorie A+"
    A = "A", "Catégorie A (cadre)"
    B = "B", "Catégorie B (profession intermédiaire)"
    C = "C", "Catégorie C (employé)"
    HORS_CATEGORIE = "HORS_CATEGORIE", "Hors catégorie"
