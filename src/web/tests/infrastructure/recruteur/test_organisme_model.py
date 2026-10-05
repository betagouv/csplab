from uuid import UUID

from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel

NB_ETAPES_PAR_DEFAUT = 6


def test_initialize_default_etapes_sets_ordered_defaults():
    organisme = OrganismeModel()

    organisme.initialize_default_etapes()

    assert [(e["categorie"], e["nom"]) for e in organisme.etapes] == [
        ("entree", "Réception des candidatures"),
        ("en_cours", "Présélection"),
        ("en_cours", "Entretien"),
        ("en_cours", "Proposition"),
        ("refus", "Refus"),
        ("accepte", "Recrutement"),
    ]


def test_initialize_default_etapes_gives_distinct_uuids():
    organisme = OrganismeModel()

    organisme.initialize_default_etapes()

    ids = {UUID(e["entity_id"]) for e in organisme.etapes}
    assert len(ids) == NB_ETAPES_PAR_DEFAUT
