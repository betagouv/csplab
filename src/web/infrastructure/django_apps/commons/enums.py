from django.db import models


class Canal(models.TextChoices):
    ADMIN = "admin", "Admin Django"
    JWT = "jwt", "API (JWT)"
    APIKEY = "apikey", "API (clé d'API)"
    PROCONNECT = "proconnect", "ProConnect"


class Resultat(models.TextChoices):
    SUCCES = "succes", "Succès"
    ECHEC = "echec", "Échec"
