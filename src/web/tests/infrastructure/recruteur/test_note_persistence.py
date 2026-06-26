from uuid import UUID, uuid4

import pytest
from faker import Faker

from domain.recruteur.errors.note_errors import CandidatureIntrouvable, NoteIntrouvable
from infrastructure.repositories.recruteur.postgres_note_repository import (
    PostgresNoteRepository,
)
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.identite.candidat_factory import CandidatFactory
from tests.factories.recruteur.note_factory import NoteFactory
from tests.factories.referentiel.offer_factory import OfferFactory

fake = Faker("fr_FR")


@pytest.fixture(name="candidature_id")
def candidature_id_fixture(db) -> UUID:
    # TODO : refactor into CandidatureFactory
    offre = OfferFactory.create_model()
    candidat = CandidatFactory.create_model()
    candidature = CandidatureFactory.build_model(
        candidat_id=candidat.utilisateur_id, offre_id=offre.id
    )
    return candidature.id


@pytest.fixture(name="agent_id")
def agent_id_fixture(db) -> UUID:
    return UUID(AgentFactory.create_model().utilisateur_id)


def test_create_and_get_by_id_roundtrip(candidature_id, agent_id) -> None:
    repository = PostgresNoteRepository()
    note = NoteFactory.create_entity(
        candidature_id=candidature_id, publie_par_id=agent_id
    )

    repository.create(note)
    fetched = repository.get_by_id(note.entity_id)

    assert fetched.entity_id == note.entity_id
    assert str(fetched.candidature_id) == candidature_id
    assert fetched.publie_par_id == agent_id
    assert fetched.message == note.message
    assert fetched.supprimee_le is None


def test_get_by_id_raises_when_missing(db) -> None:
    repository = PostgresNoteRepository()

    with pytest.raises(NoteIntrouvable):
        repository.get_by_id(uuid4())


def test_create_raises_when_candidature_unknown(agent_id) -> None:
    repository = PostgresNoteRepository()
    note = NoteFactory.create_entity(
        candidature_id=uuid4(),
        publie_par_id=agent_id,
    )

    breakpoint()
    with pytest.raises(CandidatureIntrouvable):
        repository.create(note)


def test_save_persists_message_edit(candidature_id, agent_id) -> None:
    repository = PostgresNoteRepository()
    model = NoteFactory.create_model(
        candidature_id=candidature_id, publie_par_id=agent_id
    )
    note = repository.get_by_id(model.id)

    nouveau_message = fake.sentence()
    note.modifier_message(message=nouveau_message, mis_a_jour_par_id=agent_id)
    repository.save(note)

    assert repository.get_by_id(model.id).message == nouveau_message


def test_soft_delete_excludes_from_listing_but_keeps_row(
    candidature_id, agent_id
) -> None:
    repository = PostgresNoteRepository()
    model = NoteFactory.create_model(
        candidature_id=candidature_id, publie_par_id=agent_id
    )
    note = repository.get_by_id(model.id)

    note.supprimer(supprime_par_id=agent_id)
    repository.save(note)

    assert repository.list_by_candidature(candidature_id) == []
    # row is kept (soft delete): still fetchable by id
    fetched = repository.get_by_id(model.id)
    assert fetched.supprimee_le is not None
    assert fetched.supprimee_par_id == agent_id


def test_list_by_candidature_returns_only_its_notes_ordered(
    candidature_id, agent_id
) -> None:
    # TODO : refactor
    offre = OfferFactory.create_model()
    other_candidat = CandidatFactory.create_model()
    other_candidature = CandidatureFactory.build_model(
        candidat_id=other_candidat.utilisateur_id, offre_id=offre.id
    ).id

    note_a = NoteFactory.create_model(
        candidature_id=candidature_id, publie_par_id=agent_id
    )
    note_b = NoteFactory.create_model(
        candidature_id=candidature_id, publie_par_id=agent_id
    )
    NoteFactory.create_model(candidature_id=other_candidature, publie_par_id=agent_id)
    repository = PostgresNoteRepository()

    notes = repository.list_by_candidature(candidature_id)

    assert [n.entity_id for n in notes] == [note_a.id, note_b.id]
