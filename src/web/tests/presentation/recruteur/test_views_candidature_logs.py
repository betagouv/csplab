from uuid import uuid4

from django.urls import reverse
from rest_framework import status

from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)
from presentation.recruteur.views.candidature_logs import _EVENEMENTS

NOMBRE_LOGS_SEED = 1 + len(_EVENEMENTS)
TAILLE_PAGE_LIMITEE = 2


def _url(organisme_uuid, recrutement_uuid, candidature_uuid):
    return reverse(
        "recruteur:organisme-recrutement-candidature-logs",
        kwargs={
            "organisme_uuid": organisme_uuid,
            "recrutement_uuid": recrutement_uuid,
            "candidature_uuid": candidature_uuid,
        },
    )


class TestCandidatureLogsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(_url(uuid4(), uuid4(), uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_limit_param_caps_page_size(self, authenticated_client):
        organisme = OrganismeDjangoFactory()
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)

        response = authenticated_client.get(
            _url(organisme.id, recrutement.pk, candidature.id),
            {"limit": TAILLE_PAGE_LIMITEE},
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["count"] == NOMBRE_LOGS_SEED
        assert len(body["results"]) == TAILLE_PAGE_LIMITEE
        assert body["next"] is not None
