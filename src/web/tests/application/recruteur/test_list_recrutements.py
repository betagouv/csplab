from datetime import UTC, datetime

import pytest

from application.recruteur.services.list_recrutements import (
    list_actives_recrutements,
    list_archived_recrutements,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

pytestmark = pytest.mark.usefixtures("db")

EXPECTED_PAR_CATEGORIE = 2
EXPECTED_TOTAL = 4
EXPECTED_RESPONSABLES = 1
PAGE_SIZE = 2
NB_RECRUTEMENTS = 5


class TestListRecrutements:
    def _supervisor(self):
        return create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)

    @pytest.mark.parametrize(
        ("lister", "archived"),
        [(list_actives_recrutements, False), (list_archived_recrutements, True)],
        ids=["actifs", "archives"],
    )
    def test_only_active_responsables_are_listed(self, lister, archived):
        agent, organisme = self._supervisor()
        recrutement = RecrutementDjangoFactory(
            offre_archivee=archived,
            organisme=organisme,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )
        responsable = recrutement.agents_liaisons.get().agent
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, role=AgentRecrutementRole.CONTRIBUTEUR.value
        )
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            role=AgentRecrutementRole.RESPONSABLE.value,
            date_revocation=datetime(2026, 1, 1, tzinfo=UTC),
        )

        items = lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

        assert [r.nom for r in items[0].responsables] == [
            responsable.utilisateur.get_full_name()
        ]

    def test_responsable_without_identity_falls_back_on_email(self):
        agent, organisme = self._supervisor()
        sans_identite = AgentDjangoFactory(
            utilisateur__first_name="", utilisateur__last_name=""
        )
        RecrutementDjangoFactory(
            organisme=organisme,
            agent_link__agent=sans_identite,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )

        items = list_actives_recrutements(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

        assert [r.nom for r in items[0].responsables] == [
            sans_identite.utilisateur.email
        ]

    def test_actif_without_candidature_falls_back_on_publication_date(self):
        agent, organisme = self._supervisor()
        offre = OfferDjangoFactory(publication_date=datetime(2024, 3, 1, tzinfo=UTC))
        RecrutementDjangoFactory(
            offre=offre,
            organisme=organisme,
            agent_link__agent=agent,
            etapes=EtapeRecrutementFactory.create_entity_batch(),
        )

        items = list_actives_recrutements(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

        assert items[0].candidatures_total == 0
        assert items[0].derniere_activite == offre.publication_date

    def test_actif_derniere_activite_is_latest_candidature_update(self):
        agent, organisme = self._supervisor()
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        etape = recrutement.etapes.get(categorie=CategorieEtapeRecrutement.ENTREE.value)
        CandidatureDjangoFactory(etape=etape)
        latest = CandidatureDjangoFactory(etape=etape)

        items = list_actives_recrutements(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

        latest.refresh_from_db()
        assert items[0].derniere_activite == latest.updated_at
        assert items[0].derniere_activite > recrutement.offre.publication_date

    def test_actif_counts_are_not_inflated_by_other_joins(self):
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, role=AgentRecrutementRole.CONTRIBUTEUR.value
        )
        for categorie in (
            CategorieEtapeRecrutement.ENTREE,
            CategorieEtapeRecrutement.EN_COURS,
        ):
            etape = recrutement.etapes.get(categorie=categorie.value)
            CandidatureDjangoFactory.create_batch(2, etape=etape)

        items = list_actives_recrutements(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

        assert items[0].candidatures_total == EXPECTED_TOTAL
        assert items[0].candidatures_a_traiter == EXPECTED_PAR_CATEGORIE
        assert items[0].candidatures_en_cours == EXPECTED_PAR_CATEGORIE
        assert len(items[0].responsables) == EXPECTED_RESPONSABLES

    def test_archive_without_accepted_candidature(self):
        agent, organisme = self._supervisor()
        RecrutementDjangoFactory(
            offre_archivee=True, organisme=organisme, agent_link__agent=agent
        )

        items = list_archived_recrutements(
            organisme_id=organisme.id, utilisateur=agent.utilisateur
        )

        assert items[0].finalise is False
        assert items[0].nom_candidat_recrute is None

    def test_unknown_organisme_raises(self):
        agent, _ = self._supervisor()

        with pytest.raises(OrganismeNexistePas):
            list_actives_recrutements(
                organisme_id=OrganismeDjangoFactory.build().id,
                utilisateur=agent.utilisateur,
            )


@pytest.mark.parametrize(
    ("lister", "archived"),
    [(list_actives_recrutements, False), (list_archived_recrutements, True)],
    ids=["actifs", "archives"],
)
class TestListRecrutementsRbac:
    def _create_recrutements(self, agent, organisme, archived):
        in_org = RecrutementDjangoFactory(offre_archivee=archived, organisme=organisme)
        in_org_with_role = RecrutementDjangoFactory(
            offre_archivee=archived,
            organisme=organisme,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        in_other_org = RecrutementDjangoFactory(offre_archivee=archived)
        in_other_org_with_role = RecrutementDjangoFactory(
            offre_archivee=archived,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        return in_org, in_org_with_role, in_other_org, in_other_org_with_role

    def test_superviseur_sees_all_recrutements_of_organisme(self, lister, archived):
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )
        in_org, in_org_with_role, in_other_org, in_other_org_with_role = (
            self._create_recrutements(agent, organisme, archived)
        )

        results = lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

        assert set(results) == {in_org, in_org_with_role}
        assert in_other_org not in results
        assert in_other_org_with_role not in results

    def test_agent_sees_only_its_recrutements(self, lister, archived):
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        _, in_org_with_role, _, _ = self._create_recrutements(
            agent, organisme, archived
        )

        results = lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

        assert list(results) == [in_org_with_role]

    def test_non_member_is_denied(self, lister, archived):
        agent = AgentDjangoFactory()
        organisme = OrganismeDjangoFactory()
        self._create_recrutements(agent, organisme, archived)

        with pytest.raises(AccesOrganismeRefuse):
            lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

    @pytest.mark.parametrize(
        "organisme_role",
        [None, AgentOrganismeRole.AGENT],
        ids=["no_organisme_role", "agent_role"],
    )
    def test_staff_sees_all_recrutements_of_organisme(
        self, lister, archived, organisme_role
    ):
        if organisme_role is None:
            agent = AgentDjangoFactory()
            organisme = OrganismeDjangoFactory()
        else:
            agent, organisme = create_organisme_with_agent(role=organisme_role)
        in_org, in_org_with_role, _, _ = self._create_recrutements(
            agent, organisme, archived
        )
        agent.utilisateur.is_staff = True

        results = lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

        assert set(results) == {in_org, in_org_with_role}

    def test_results_are_ordered_by_offre_id(self, lister, archived):
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )
        RecrutementDjangoFactory.create_batch(
            NB_RECRUTEMENTS, offre_archivee=archived, organisme=organisme
        )

        results = lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

        ids = [r.offre_id for r in results]
        assert ids == sorted(ids)
        paginated = [
            r.offre_id
            for start in range(0, NB_RECRUTEMENTS, PAGE_SIZE)
            for r in results[start : start + PAGE_SIZE]
        ]
        assert paginated == ids

    def test_agent_revoked_from_recrutement_does_not_see_it(self, lister, archived):
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        revoked = RecrutementDjangoFactory(
            offre_archivee=archived,
            organisme=organisme,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
            agent_link__date_revocation=datetime.now(UTC),
        )
        # Autre membre actif : deux jointures laisseraient passer ce recrutement
        RecrutementAgentDjangoFactory(
            recrutement=revoked, role=AgentRecrutementRole.RESPONSABLE.value
        )
        witness = RecrutementDjangoFactory(
            offre_archivee=archived,
            organisme=organisme,
            agent_link__agent=agent,
            agent_link__role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )

        results = lister(organisme_id=organisme.id, utilisateur=agent.utilisateur)

        assert list(results) == [witness]
