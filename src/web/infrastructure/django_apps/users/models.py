from django.contrib.auth.models import AbstractUser
from django.db import models

from domain.identite.entities.agent import Agent
from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_role import OrganismeRole


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

    def to_entity(
        self, organisme_roles: list[OrganismeRole] | None = None
    ) -> Utilisateur:
        return Utilisateur(
            entity_id=self.username,
            email=self.email,
            prenom=self.first_name,
            nom=self.last_name,
            is_superuser=self.is_superuser,
            organisme_roles=organisme_roles or [],
        )

    @classmethod
    def from_entity(cls, utilisateur: Utilisateur) -> "UserModel":
        return cls(
            username=utilisateur.entity_id,
            email=utilisateur.email,
            first_name=utilisateur.prenom,
            last_name=utilisateur.nom,
            is_superuser=utilisateur.is_superuser,
        )

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
