from django.db.models import TextChoices


class SourceType(TextChoices):
    TALENTSOFT = "talentsoft", "talentsoft"
    API = "api", "api"
