from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel


def a_un_rattachement_actif(user) -> bool:
    return OrganismeAgentModel.objects.by_agent(user.username).exists()
