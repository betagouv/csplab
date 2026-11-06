from django.db import models


class Canal(models.TextChoices):
    ADMIN = "admin", "Admin Django"
    JWT = "jwt", "API (JWT)"
    APIKEY = "apikey", "API (clé d'API)"
    PROCONNECT = "proconnect", "ProConnect"


class Resultat(models.TextChoices):
    SUCCES = "succes", "Succès"
    ECHEC = "echec", "Échec"


class Metric(models.TextChoices):
    PUBLISHED_OFFERS = "nb_offres_publiees", "Offres publiées"
    ARCHIVED_OFFERS = "nb_offres_archivees", "Offres archivées"
