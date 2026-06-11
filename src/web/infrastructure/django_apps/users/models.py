from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.db import models

from domain.identite.entities.utilisateurs import Utilisateur


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(
        unique=True,
        null=False,
        blank=False,
        editable=False,
        max_length=36,
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

    def to_entity(self) -> Utilisateur:
        return Utilisateur(
            entity_id=UUID(self.username),
            email=self.email,
            prenom=self.first_name,
            nom=self.last_name,
        )

    @classmethod
    def from_entity(cls, utilisateur: Utilisateur) -> "UserModel":
        return cls(
            username=str(utilisateur.entity_id),
            email=utilisateur.email,
            first_name=utilisateur.prenom,
            last_name=utilisateur.nom,
        )

    def __str__(self):
        return self.username
