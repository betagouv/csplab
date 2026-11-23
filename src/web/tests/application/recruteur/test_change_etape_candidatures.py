from unittest.mock import patch

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from application.recruteur.services.change_etape_candidatures import (
    change_etape_candidatures,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)


def test_rolls_back_every_write_when_the_last_audit_log_fails(db):
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    origine, cible = list(EtapeModel.objects.filter(recrutement=recrutement))[:2]
    candidatures = CandidatureDjangoFactory.create_batch(2, etape=origine)
    log_action = AuditLogWriter.log_action
    appels = []

    def echoue_au_dernier_appel(writer, **kwargs):
        appels.append(kwargs["event_name"])
        if kwargs["event_name"] == "EtapeCandidaturesChangees":
            raise RuntimeError("audit log write failed")
        log_action(writer, **kwargs)

    with (
        patch.object(AuditLogWriter, "log_action", new=echoue_au_dernier_appel),
        pytest.raises(RuntimeError),
    ):
        change_etape_candidatures(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=superviseur.utilisateur,
            etape_cible_id=cible.id,
            candidature_ids=[candidature.id for candidature in candidatures],
        )

    assert appels == [
        "CandidatureEtapeModifiee",
        "CandidatureEtapeModifiee",
        "EtapeCandidaturesChangees",
    ]
    assert set(
        CandidatureModel.objects.values_list("etape_id", "updated_by_recruteur")
    ) == {(origine.id, None)}
    assert not AuditLogModel.objects.exists()


def test_locks_the_recrutement_and_the_candidatures(db):
    superviseur, organisme = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    origine, cible = list(EtapeModel.objects.filter(recrutement=recrutement))[:2]
    candidature = CandidatureDjangoFactory(etape=origine)

    with CaptureQueriesContext(connection) as requetes:
        change_etape_candidatures(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=superviseur.utilisateur,
            etape_cible_id=cible.id,
            candidature_ids=[candidature.id],
        )

    verrous = [
        requete["sql"][requete["sql"].index(" FOR ") :]
        for requete in requetes.captured_queries
        if " FOR " in requete["sql"]
    ]
    assert sorted(verrous) == [
        ' FOR NO KEY UPDATE OF "recrutement"',
        ' FOR UPDATE OF "candidature"',
    ]
