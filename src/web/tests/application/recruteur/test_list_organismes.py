from datetime import timedelta

import pytest
from django.utils import timezone

from application.recruteur.services.list_organismes import list_organismes
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)


@pytest.fixture(name="staff")
def staff_fixture(db):
    return UtilisateurDjangoFactory(is_staff=True)


def test_counts_agents_and_offers_without_join_inflation(staff):
    organisme = OrganismeDjangoFactory()
    OrganismeAgentDjangoFactory.create_batch(2, organisme=organisme)
    RecrutementDjangoFactory.create_batch(3, organisme=organisme)

    result = list_organismes(utilisateur=staff).get(pk=organisme.pk)

    assert result.number_agents == 2  # noqa: PLR2004
    assert result.number_published_offers == 3  # noqa: PLR2004


def test_does_not_count_revoked_agents(staff):
    _, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    OrganismeAgentDjangoFactory(organisme=organisme, date_revocation=timezone.now())

    result = list_organismes(utilisateur=staff).get(pk=organisme.pk)

    assert result.number_agents == 1


def test_last_activity_is_latest_agent_update(staff):
    _, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    liaison = organisme.agents_liaisons.get()
    liaison.__class__.objects.filter(pk=liaison.pk).update(
        updated_at=organisme.updated_at + timedelta(days=1)
    )
    liaison.refresh_from_db()

    result = list_organismes(utilisateur=staff).get(pk=organisme.pk)

    assert result.last_activity_date == liaison.updated_at


def test_orders_by_most_recently_updated(staff):
    older, newer = OrganismeDjangoFactory.create_batch(2)

    result = list(list_organismes(utilisateur=staff))

    assert result.index(newer) < result.index(older)


def test_excludes_supprimes(staff):
    actif = OrganismeDjangoFactory()
    OrganismeDjangoFactory(supprime_le=timezone.now())

    assert list(list_organismes(utilisateur=staff)) == [actif]


def test_refuses_non_staff(db):
    with pytest.raises(OperationOrganismeRefusee):
        list_organismes(utilisateur=UtilisateurDjangoFactory(is_staff=False))


def test_evaluates_in_a_constant_number_of_queries(staff, django_assert_num_queries):
    for organisme in OrganismeDjangoFactory.create_batch(3):
        OrganismeAgentDjangoFactory(organisme=organisme)
        OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.SUPERVISEUR.value
        )
        RecrutementDjangoFactory(organisme=organisme)

    with django_assert_num_queries(2):  # organismes + prefetch superviseurs
        result = list(list_organismes(utilisateur=staff))
        assert all(o.number_agents and o.number_published_offers for o in result)
        # same traversal as the serializer: a lazy load here would add queries
        utilisateurs = [
            liaison.agent.utilisateur
            for o in result
            for liaison in o.superviseurs_actifs
        ]
        assert len(utilisateurs) == len(result)


def test_counts_stay_exact_with_many_agents_and_offers_per_organisme(staff):
    organisme, other = OrganismeDjangoFactory.create_batch(2)
    OrganismeAgentDjangoFactory.create_batch(4, organisme=organisme)
    RecrutementDjangoFactory.create_batch(5, organisme=organisme)
    OrganismeAgentDjangoFactory(organisme=other)

    result = {o.pk: o for o in list_organismes(utilisateur=staff)}

    assert result[organisme.pk].number_agents == 4  # noqa: PLR2004
    assert result[organisme.pk].number_published_offers == 5  # noqa: PLR2004
    assert result[other.pk].number_agents == 1
    assert result[other.pk].number_published_offers == 0


def test_counts_are_zero_without_agents_nor_offers(staff):
    organisme = OrganismeDjangoFactory()

    result = list_organismes(utilisateur=staff).get(pk=organisme.pk)

    assert result.number_agents == 0
    assert result.number_published_offers == 0
    assert result.last_activity_date == organisme.updated_at


def test_does_not_count_archived_offers(staff):
    organisme = OrganismeDjangoFactory()
    OrganismeAgentDjangoFactory(organisme=organisme)
    RecrutementDjangoFactory.create_batch(2, organisme=organisme, offre_archivee=True)

    result = list_organismes(utilisateur=staff).get(pk=organisme.pk)

    assert result.number_published_offers == 0
    assert result.number_agents == 1


def test_query_count_does_not_grow_with_agents_and_offers_per_organisme(
    staff, django_assert_num_queries
):
    organisme = OrganismeDjangoFactory()

    with django_assert_num_queries(2):  # organismes + prefetch superviseurs
        for o in list_organismes(utilisateur=staff):
            _ = (o.number_agents, o.number_published_offers, o.superviseurs_actifs)

    OrganismeAgentDjangoFactory.create_batch(10, organisme=organisme)
    OrganismeAgentDjangoFactory.create_batch(
        3, organisme=organisme, role=AgentOrganismeRole.SUPERVISEUR.value
    )
    RecrutementDjangoFactory.create_batch(10, organisme=organisme)

    with django_assert_num_queries(2):
        for o in list_organismes(utilisateur=staff):
            _ = (o.number_agents, o.number_published_offers, o.superviseurs_actifs)
