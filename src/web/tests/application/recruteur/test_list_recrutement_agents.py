from django.utils import timezone

from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)


def test_by_recrutement_excludes_revoked_agents(db):
    # RecrutementDjangoFactory auto-creates one active RecrutementAgentModel via its
    # `agent_link` RelatedFactory.
    recrutement = RecrutementDjangoFactory()
    active_id = RecrutementAgentModel.objects.get(recrutement=recrutement).id
    revoked = RecrutementAgentDjangoFactory(
        recrutement=recrutement, date_revocation=timezone.now()
    )

    agent_ids = set(
        RecrutementAgentModel.objects.by_recrutement(recrutement.pk).values_list(
            "id", flat=True
        )
    )

    assert agent_ids == {active_id}
    assert revoked.id not in agent_ids
