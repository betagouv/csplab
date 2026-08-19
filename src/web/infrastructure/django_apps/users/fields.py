from django.db import models

from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
    ProfilCandidatModel,
)


def agent_fk(
    *, related_name: str, on_delete=models.PROTECT
) -> "models.ForeignKey[ProfilAgentModel, ProfilAgentModel]":
    return models.ForeignKey(
        ProfilAgentModel,
        to_field="utilisateur_id",
        on_delete=on_delete,
        related_name=related_name,
    )


def candidat_fk(
    *, related_name: str, on_delete=models.PROTECT
) -> "models.ForeignKey[ProfilCandidatModel, ProfilCandidatModel]":
    return models.ForeignKey(
        ProfilCandidatModel,
        to_field="utilisateur_id",
        on_delete=on_delete,
        related_name=related_name,
    )
