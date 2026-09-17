from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower, Trim

from domain.identite.entities.agent import Agent
from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.email import normalize_email


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

    @classmethod
    def from_entity(
        cls, utilisateur: Utilisateur, candidat: Candidat
    ) -> "ProfilCandidatModel":
        return cls(
            utilisateur_id=utilisateur.entity_id,
            resume=candidat.resume,
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
