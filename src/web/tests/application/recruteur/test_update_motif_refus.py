from unittest.mock import patch

import pytest

from application.recruteur.services.update_motif_refus import update_motif_refus
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
)


class TestUpdateMotifRefus:
    @patch.object(AuditLogWriter, "log_action", side_effect=RuntimeError)
    def test_rolls_back_when_audit_log_fails(self, _log_action, test_user):
        _, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent(
                role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
            )
        )
        refus = EtapeModel.objects.filter(
            recrutement=recrutement, categorie=CategorieEtapeRecrutement.REFUS.value
        ).first()
        CandidatureModel.objects.filter(pk=candidature.pk).update(
            etape=refus, motif_refus=MotifRefus.EXPERIENCE_INSUFFISANTE.value
        )

        with pytest.raises(RuntimeError):
            update_motif_refus(
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                candidature_id=candidature.id,
                motif_refus=MotifRefus.AUTRE.value,
                utilisateur=test_user,
            )

        candidature.refresh_from_db()
        assert candidature.motif_refus == MotifRefus.EXPERIENCE_INSUFFISANTE.value
