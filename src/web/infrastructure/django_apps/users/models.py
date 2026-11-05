from typing import ClassVar
from uuid import uuid4

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Exists, F, Func, OuterRef, Q
from django.db.models.functions import Lower, Trim

from domain.identite.entities.agent import Agent
from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.email import normalize_email
from infrastructure.django_apps.utils.ip import (
    IPAddressInput,
    ip_in_networks,
    normalize_network,
)
from infrastructure.django_apps.utils.models import BaseDatedModel

DEMO_CANDIDAT_EMAIL_DOMAIN = "@demo.candidat.fr"


class UserQuerySet(models.QuerySet):
    def avec_restriction_ip(self) -> "UserQuerySet":
        return self.annotate(
            ip_restricted=Exists(
                AllowedNetworkModel.objects.filter(user=OuterRef("pk"))
            )
        )


class UserModelManager(UserManager):
    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.UUIDField(  # type: ignore[assignment]
        unique=True,
        null=False,
        blank=False,
        editable=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    objects: ClassVar[UserModelManager] = UserModelManager()  # type: ignore[assignment]

    sources = models.ManyToManyField(
        "ingestion.SourceModel",
        blank=True,
        related_name="users",
        verbose_name="Sources",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.CheckConstraint(
                condition=Q(email=Trim(Lower("email"))),
                name="users_email_is_lowercase",
            )
        ]

    def save(self, *args, **kwargs):
        # Django has a hook for this, AbstractUser.clean(), but it only runs on
        # full_clean(), which save() never calls.
        self.email = normalize_email(self.email)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def api_ip_is_allowed(self, ip: IPAddressInput | None) -> bool:
        # No network: no restriction. Otherwise an unknown IP is refused too.
        networks = [network.cidr for network in self.allowed_networks.all()]
        return not networks or ip_in_networks(ip, networks)


class CanonicalCidr(Func):
    template = "(%(expressions)s)::cidr::text"
    output_field = models.CharField()


class AllowedNetworkModel(BaseDatedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="allowed_networks",
    )
    cidr = models.CharField(
        "IP ou plage CIDR",
        max_length=43,
        help_text="IP (203.0.113.10) ou plage CIDR (203.0.113.0/24, 2001:db8::/48).",
    )
    label = models.CharField(
        "Libellé",
        max_length=255,
        help_text="Origine de la plage, ex. « NAT prod partenaire X ».",
    )

    class Meta:
        verbose_name = "Réseau autorisé pour l'API"
        verbose_name_plural = "Réseaux autorisés pour l'API"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "cidr"], name="allowed_networks_user_cidr_uniq"
            ),
            # Postgres refuses an invalid range or one with host bits set.
            models.CheckConstraint(
                condition=Q(cidr=CanonicalCidr(F("cidr"))),
                name="allowed_networks_cidr_is_canonical",
            ),
        ]

    def clean(self) -> None:
        if not self.cidr:
            return
        try:
            self.cidr = normalize_network(self.cidr)
        except ValueError as e:
            raise ValidationError(
                {"cidr": "Saisissez une adresse IP ou une plage CIDR valide."}
            ) from e

    def save(self, *args, **kwargs):
        self.cidr = normalize_network(self.cidr)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cidr} ({self.label})"


class ProfilCandidatModel(models.Model):
    utilisateur = models.OneToOneField(
        UserModel,
        on_delete=models.PROTECT,
        related_name="profil_candidat",
        to_field="username",
    )
    resume = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Candidat"
        verbose_name_plural = "Profils Candidats"

    def to_entity(self) -> Candidat:
        return Candidat.build(
            entity_id=self.utilisateur.username,
            email=self.utilisateur.email,
            prenom=self.utilisateur.first_name,
            nom=self.utilisateur.last_name,
            resume=self.resume,
        )

    def __str__(self):
        return self.utilisateur.email


class ProfilAgentQuerySet(models.QuerySet):
    def par_email(self, email: str) -> "ProfilAgentQuerySet":
        return self.select_related("utilisateur").filter(
            utilisateur__email=normalize_email(email)
        )


class ProfilAgentModel(models.Model):
    utilisateur = models.OneToOneField(
        UserModel,
        on_delete=models.PROTECT,
        related_name="profil_agent",
        to_field="username",
    )
    intitule_poste = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfilAgentQuerySet.as_manager()

    class Meta:
        verbose_name = "Profil Agent"
        verbose_name_plural = "Profils Agents"

    def to_entity(self) -> Agent:
        return Agent.build(
            entity_id=self.utilisateur.username,
            email=self.utilisateur.email,
            prenom=self.utilisateur.first_name,
            nom=self.utilisateur.last_name,
            intitule_poste=self.intitule_poste,
        )

    @classmethod
    def from_entity(cls, utilisateur: Utilisateur, agent: Agent) -> "ProfilAgentModel":
        return cls(
            utilisateur_id=utilisateur.entity_id,
            intitule_poste=agent.intitule_poste,
        )

    def __str__(self):
        return self.utilisateur.email
