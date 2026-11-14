from application.recruteur.services.add_candidature_tag import add_candidature_tag
from infrastructure.django_apps.tag.models import CandidatureTagModel, TagCategory
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.tag.tag_django_factory import TagDjangoFactory


# transactional_db : `db` masquerait un select_for_update hors transaction.atomic()
def test_add_candidature_tag_runs_in_its_own_transaction(transactional_db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    tag = TagDjangoFactory(organisme=organisme, category=TagCategory.CANDIDATURE)

    add_candidature_tag(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.id,
        tag_id=tag.id,
        utilisateur=agent.utilisateur,
    )

    assert list(
        CandidatureTagModel.objects.filter(candidature=candidature).values_list(
            "tag_id", flat=True
        )
    ) == [tag.id]
