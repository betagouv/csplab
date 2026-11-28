import operator
from collections.abc import Iterable
from datetime import timedelta
from functools import reduce
from uuid import UUID

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Exists, F, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.ingestion.models.talentsoft_organisme import (
    TalentsoftOrganismeModel,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.django_apps.utils.models import BaseDatedModel, related_model

SEARCH_CONFIG = "french"
KEYWORDS_SEARCH_WEIGHTS = {
    "A": ("title",),
    "B": ("long_title",),
    "C": ("mission", "profile", "organization", "employer", "complements"),
}


class OfferQuerySet(models.QuerySet):
    def by_source(self, source_id: UUID) -> "OfferQuerySet":
        return self.filter(source_id=source_id)

    def actives(self) -> "OfferQuerySet":
        return self.filter(archived_at__isnull=True)

    def archived(self) -> "OfferQuerySet":
        return self.filter(archived_at__isnull=False)

    def by_references(self, references: Iterable[str]) -> "OfferQuerySet":
        return self.filter(reference__in=references)

    def with_localisations(self) -> "OfferQuerySet":
        return self.prefetch_related("localisations")

    def with_organisation_siret(self) -> "OfferQuerySet":
        return self.annotate(
            organisation_siret=Coalesce(
                "organisme__siret", "talentsoft_organisme_entity_code__organisme__siret"
            )
        )

    def with_metier_libelle(self) -> "OfferQuerySet":
        metiers = MetierModel.objects.filter(
            offer_family_code=OuterRef("code_emploi_csp"),
            job_family_referential=OuterRef("job_family_referential"),
        ).stable_order()
        return self.annotate(
            metier_libelle=Subquery(metiers.values("libelle_long")[:1])
        )

    def with_localisation_in(
        self,
        *,
        regions: Iterable[str] = (),
        departments: Iterable[str] = (),
        countries: Iterable[str] = (),
        areas: Iterable[str] = (),
    ) -> "OfferQuerySet":
        localisations = self._localisations().located_in(
            regions=regions, departments=departments, countries=countries, areas=areas
        )
        if localisations is None:
            return self
        return self.filter(Exists(localisations))

    def with_localisation_within(
        self, latitude: float, longitude: float, radius_km: float
    ) -> "OfferQuerySet":
        return self.filter(
            Exists(self._localisations().within(latitude, longitude, radius_km))
        )

    def _localisations(self):
        localisation_model = related_model(self.model, "localisations")
        return localisation_model._default_manager.filter(offer=OuterRef("pk"))

    def search(self, term: str) -> "OfferQuerySet":
        if not term:
            return self
        return self.filter(Q(reference__icontains=term) | Q(title__icontains=term))

    def matching_keywords(self, keywords: str) -> "OfferQuerySet":
        vectors = [
            SearchVector(*fields, weight=weight, config=SEARCH_CONFIG)
            for weight, fields in KEYWORDS_SEARCH_WEIGHTS.items()
        ]
        search_vector = reduce(operator.add, vectors)
        search_query = SearchQuery(keywords, config=SEARCH_CONFIG)
        return self.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query)

    def filtered(
        self,
        active: bool,
        category: list[Category] | None = None,
        verse: list[Verse] | None = None,
        offer_nature: list[OfferNature] | None = None,
        experience_level: list[ExperienceLevel] | None = None,
        management: list[Management] | None = None,
        working_place: list[WorkingPlace] | None = None,
        region: list[Region] | None = None,
        department: list[Department] | None = None,
        country: list[Country] | None = None,
        area: list[GeographicalArea] | None = None,
        domain: list[str] | None = None,
        organization: list[str] | None = None,
        published_within_days: int | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        radius_km: int | None = None,
        keywords: str | None = None,
    ) -> "OfferQuerySet":
        qs = self.filter(archived_at__isnull=active)
        for lookup, values in (
            ("categories__overlap", [c.value for c in category or []]),
            ("verse__in", [v.value for v in verse or []]),
            ("offer_nature__in", [n.value for n in offer_nature or []]),
            ("criteria__experience__in", [e.name for e in experience_level or []]),
            ("conditions__management__in", [m.name for m in management or []]),
            ("conditions__lieu_de_travail__in", [w.name for w in working_place or []]),
            ("functional_area_code__in", [str(d) for d in domain or []]),
        ):
            if values:
                qs = qs.filter(**{lookup: values})
        qs = qs.with_localisation_in(
            regions=[r.code for r in region or []],
            departments=[d.code for d in department or []],
            countries=[str(c) for c in country or []],
            areas=[a.value for a in area or []],
        )

        if organization:
            qs = qs.filter(
                talentsoft_organisme_entity_code__in=TalentsoftOrganismeModel.objects.with_descendants_of(
                    organization
                ).values("entity_code")
            )

        if published_within_days is not None:
            since = timezone.now() - timedelta(days=abs(published_within_days))
            qs = qs.filter(publication_date__gte=since)

        if latitude is not None and longitude is not None and radius_km is not None:
            qs = qs.with_localisation_within(latitude, longitude, radius_km)

        if keywords:
            return qs.matching_keywords(keywords).order_by("-rank", "-updated_at")
        return qs.order_by("-updated_at")


class OfferModel(BaseDatedModel):
    # Offer nature choices from OfferNature enum
    OFFER_NATURE_CHOICES = [(ct.value, ct.name) for ct in OfferNature]

    # Category choices from Category enum
    CATEGORY_CHOICES = [(cat.value, cat.name) for cat in Category]

    # Verse choices from Verse enum
    VERSE_CHOICES = [(v.value, v.name) for v in Verse]

    reference = models.CharField(max_length=100, null=False, blank=False)
    verse = models.CharField(
        max_length=20, choices=VERSE_CHOICES, null=True, blank=True
    )
    title = models.CharField(max_length=500)
    profile = models.TextField()
    mission = models.TextField()
    categories = ArrayField(
        models.CharField(max_length=20, choices=CATEGORY_CHOICES),
    )
    offer_nature = models.CharField(
        max_length=25, choices=OFFER_NATURE_CHOICES, null=True, blank=True
    )
    organization = models.CharField(max_length=500)
    offer_url = models.URLField(null=True, blank=True)
    code_emploi_csp = models.CharField(max_length=50, null=True, blank=True)
    job_family_referential = models.CharField(max_length=50, null=True, blank=True)
    local_job_code = models.CharField(max_length=50, null=True, blank=True)
    functional_area_code = models.CharField(max_length=3, null=True, blank=True)
    source = models.ForeignKey(
        SourceModel,
        to_field="source_id",
        on_delete=models.PROTECT,
        related_name="offers",
    )
    talentsoft_organisme_entity_code = models.ForeignKey(
        TalentsoftOrganismeModel,
        to_field="entity_code",
        on_delete=models.PROTECT,
        related_name="offers",
        null=True,
        blank=True,
    )
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.PROTECT,
        related_name="offers",
        null=True,
        blank=True,
    )

    long_title = models.CharField(max_length=1500, null=True, blank=True)
    application_url = models.URLField(null=True, blank=True)
    application_email = models.EmailField(null=True, blank=True)
    contract_kind = models.CharField(max_length=20, null=True, blank=True)
    job_vacancy = models.CharField(max_length=50, null=True, blank=True)
    employer = models.TextField(null=True, blank=True)
    complements = models.TextField(null=True, blank=True)
    exercise_conditions = models.TextField(null=True, blank=True)
    service_description = models.TextField(null=True, blank=True)
    criteria = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    conditions = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    contacts = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)

    # Date fields
    publication_date = models.DateTimeField()
    end_publication_date = models.DateTimeField(null=True, blank=True)
    beginning_date = models.DateTimeField(null=True, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    job_vacancy_date = models.DateTimeField(null=True, blank=True)
    processing = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    objects = OfferQuerySet.as_manager()

    class Meta:
        db_table = "offers"
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        constraints = [
            models.UniqueConstraint(
                fields=["reference", "source_id"],
                name="offers_reference_source_id_unique",
            ),
            # Article D.311-8 of the CGFP: an offer has at least one category.
            models.CheckConstraint(
                condition=~Q(categories=[]),
                name="offer_categories_not_empty",
            ),
            # A long title copying the title would be weighted twice by the
            # full-text search.
            models.CheckConstraint(
                condition=~Q(long_title=F("title")),
                name="offer_long_title_differs_from_title",
            ),
            models.CheckConstraint(
                condition=Q(talentsoft_organisme_entity_code__isnull=True)
                | Q(organisme__isnull=True),
                name="offer_single_organisme_link",
            ),
        ]

    def __str__(self) -> str:
        return f"Offer {self.reference} ({self.source_id}) - {self.title}"

    @property
    def main_category(self) -> str | None:
        return self.categories[0] if self.categories else None
