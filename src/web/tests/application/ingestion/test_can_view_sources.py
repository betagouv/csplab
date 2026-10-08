import pytest

from application.ingestion.context_services.can_view_sources import can_view_sources
from application.ingestion.errors.application_errors_ingestion import (
    AccesSourcesRefuse,
)
from application.ingestion.services.get_offer_by_source import get_offer_by_source
from application.ingestion.services.list_authorized_sources import (
    list_authorized_sources,
)
from application.ingestion.services.list_offers_by_source import list_offers_by_source
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

USERS = {
    "user_without_profile_nor_source": (lambda s: UtilisateurDjangoFactory(), False),
    "staff_without_agent_profile": (
        lambda s: UtilisateurDjangoFactory(is_staff=True),
        False,
    ),
    "staff_with_source_without_agent_profile": (
        lambda s: UtilisateurDjangoFactory(is_staff=True, sources=[s]),
        False,
    ),
    "user_with_source_without_agent_profile": (
        lambda s: UtilisateurDjangoFactory(sources=[s]),
        True,
    ),
    "agent_without_source": (lambda s: AgentDjangoFactory().utilisateur, True),
    "staff_agent": (
        lambda s: AgentDjangoFactory(utilisateur__is_staff=True).utilisateur,
        True,
    ),
    "superuser_without_agent_profile": (
        lambda s: UtilisateurDjangoFactory(is_superuser=True),
        True,
    ),
}


@pytest.mark.parametrize(("make_user", "expected"), USERS.values(), ids=USERS.keys())
def test_can_view_sources(db, make_user, expected):
    assert can_view_sources(make_user(SourceDjangoFactory())) is expected


def _list_authorized_sources(user, source, offer):
    return list_authorized_sources(user)


def _list_offers_by_source(user, source, offer):
    return list_offers_by_source(user, source.source_id)


def _get_offer_by_source(user, source, offer):
    return get_offer_by_source(user, source.source_id, offer.id)


SERVICES = [_list_authorized_sources, _list_offers_by_source, _get_offer_by_source]


@pytest.mark.parametrize("service", SERVICES, ids=lambda f: f.__name__[1:])
def test_services_refuse_a_user_who_cannot_view_sources(db, service):
    source = SourceDjangoFactory()
    offer = OfferDjangoFactory(source=source)
    # staff rattaché à une source, mais sans profil agent : accès refusé
    user = UtilisateurDjangoFactory(is_staff=True, sources=[source])

    with pytest.raises(AccesSourcesRefuse):
        service(user, source, offer)
