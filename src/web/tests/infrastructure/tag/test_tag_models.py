import pytest
from django.db import IntegrityError, transaction

from infrastructure.django_apps.tag.models import (
    CandidatureTagModel,
    NoteTagModel,
    RecrutementAgentTagModel,
    TagCategory,
    TagModel,
)
from infrastructure.factories.tag.tag_django_factory import (
    CandidatureTagDjangoFactory,
    NoteTagDjangoFactory,
    RecrutementAgentTagDjangoFactory,
    TagDjangoFactory,
)


def test_name_is_unique_per_organisme_and_category_ignoring_case(db):
    tag = TagDjangoFactory(name="Expert")

    with pytest.raises(IntegrityError), transaction.atomic():
        TagDjangoFactory(name="EXPERT", organisme=tag.organisme, category=tag.category)


def test_same_name_allowed_in_another_category(db):
    tag = TagDjangoFactory(name="Expert", category=TagCategory.CANDIDATURE)

    other = TagDjangoFactory(
        name="Expert", organisme=tag.organisme, category=TagCategory.NOTE
    )

    assert set(TagModel.objects.filter(name="Expert")) == {tag, other}


def test_same_name_allowed_in_another_organisme(db):
    tag = TagDjangoFactory(name="Expert", category=TagCategory.CANDIDATURE)

    other = TagDjangoFactory(name="Expert", category=TagCategory.CANDIDATURE)

    assert set(TagModel.objects.filter(name="Expert")) == {tag, other}


@pytest.mark.parametrize(
    ("link_factory", "link_model"),
    [
        pytest.param(
            CandidatureTagDjangoFactory, CandidatureTagModel, id="candidature"
        ),
        pytest.param(
            RecrutementAgentTagDjangoFactory,
            RecrutementAgentTagModel,
            id="recrutement_agent",
        ),
        pytest.param(NoteTagDjangoFactory, NoteTagModel, id="note"),
    ],
)
def test_deleting_a_tag_removes_it_from_tagged_objects(db, link_factory, link_model):
    link = link_factory()

    link.tag.delete()

    assert not link_model.objects.filter(pk=link.pk).exists()


@pytest.mark.parametrize(
    ("link_factory", "target"),
    [
        pytest.param(CandidatureTagDjangoFactory, "candidature", id="candidature"),
        pytest.param(NoteTagDjangoFactory, "note", id="note"),
    ],
)
def test_tag_cannot_be_put_twice_on_the_same_object(db, link_factory, target):
    link = link_factory()

    with pytest.raises(IntegrityError), transaction.atomic():
        link_factory(tag=link.tag, **{target: getattr(link, target)})


def test_recrutement_agent_has_a_single_tag(db):
    link = RecrutementAgentTagDjangoFactory()

    with pytest.raises(IntegrityError), transaction.atomic():
        RecrutementAgentTagDjangoFactory(recrutement_agent=link.recrutement_agent)


def test_name_cannot_be_empty(db):
    with pytest.raises(IntegrityError), transaction.atomic():
        TagDjangoFactory(name="")


def test_name_cannot_have_surrounding_spaces(db):
    with pytest.raises(IntegrityError), transaction.atomic():
        TagDjangoFactory(name="Expert ")
