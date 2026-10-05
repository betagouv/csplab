from factory.django import DjangoModelFactory

from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel


class AuditLoginLogDjangoFactory(DjangoModelFactory):
    class Meta:
        model = AuditLoginLogModel

    canal = Canal.ADMIN
    resultat = Resultat.ECHEC
    utilisateur_id = None
    ip_address = "127.0.0.1"
