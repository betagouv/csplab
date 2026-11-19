from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from modelcluster.fields import ParentalManyToManyField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from presentation.pages.stub_offers import OFFERS


class StoredFile(models.Model):
    name = models.CharField(max_length=512, unique=True)
    content = models.BinaryField()
    content_type = models.CharField(max_length=256, blank=True)
    size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


IMAGE_HELP = (
    "Repli si aucune image n'est envoyée : chemin statique "
    "(ex. candidate/images/news/cyril.png) ou URL complète"
)


def picture_field():
    return models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


def resolve_image(picture, fallback):
    if picture:
        return picture.get_rendition("original").url
    return fallback


class PictureMixin:
    @property
    def display_image(self):
        return resolve_image(self.picture, self.image)


class NewsIndexPage(Page):
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["editorial.NewsPage"]
    template = "editorial/news_index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["news"] = NewsPage.objects.child_of(self).live()
        context["breadcrumb_data"] = {"links": [], "current": self.title}
        return context


class NewsPage(PictureMixin, Page):
    badge = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    picture = picture_field()
    image = models.CharField(max_length=255, blank=True, help_text=IMAGE_HELP)
    external_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    parent_page_types = ["editorial.NewsIndexPage"]
    subpage_types: list[str] = []
    template = "editorial/news_page.html"
    content_panels = [
        *Page.content_panels,
        FieldPanel("badge"),
        FieldPanel("description"),
        FieldPanel("picture"),
        FieldPanel("image"),
        FieldPanel("external_url"),
        FieldPanel("featured"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["breadcrumb_data"] = {
            "links": [{"url": self.get_parent().url, "title": "Actualités"}],
            "current": self.title,
        }
        return context


@register_snippet
class AdviceTheme(models.Model):
    slug = models.SlugField(unique=True)
    label = models.CharField(max_length=100)

    panels = [FieldPanel("slug"), FieldPanel("label")]

    def __str__(self):
        return self.label


class AdviceIndexPage(Page):
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["editorial.AdvicePage"]

    def serve(self, request, *args, **kwargs):
        return redirect(reverse("candidate:advice"))


class AdvicePage(PictureMixin, Page):
    text = models.TextField(blank=True)
    picture = picture_field()
    image = models.CharField(max_length=255, blank=True, help_text=IMAGE_HELP)
    external_url = models.URLField(blank=True)
    themes = ParentalManyToManyField(AdviceTheme, blank=True)

    parent_page_types = ["editorial.AdviceIndexPage"]
    subpage_types: list[str] = []
    template = "editorial/advice_page.html"
    content_panels = [
        *Page.content_panels,
        FieldPanel("text"),
        FieldPanel("picture"),
        FieldPanel("image"),
        FieldPanel("external_url"),
        FieldPanel("themes"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["breadcrumb_data"] = {
            "links": [
                {"url": reverse("candidate:advice"), "title": "Conseils aux candidats"}
            ],
            "current": self.title,
        }
        return context


class TerritoryIndexPage(Page):
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["editorial.TerritoryPage"]

    def serve(self, request, *args, **kwargs):
        return redirect("pages:home")


class HighlightBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    tags = blocks.ListBlock(blocks.CharBlock(), required=False)
    date = blocks.CharBlock(help_text="ex. 3/04/2026")
    picture = ImageChooserBlock(required=False)
    image = blocks.CharBlock(required=False, help_text=IMAGE_HELP)


class AssetBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    picture = ImageChooserBlock(required=False)
    image = blocks.CharBlock(required=False, help_text=IMAGE_HELP)
    caption = blocks.CharBlock(required=False)
    text = blocks.TextBlock()


class FigureBlock(blocks.StructBlock):
    value = blocks.CharBlock()
    label = blocks.CharBlock()


class LinkBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.TextBlock(required=False)
    url = blocks.URLBlock()
    picture = ImageChooserBlock(required=False)
    image = blocks.CharBlock(required=False, help_text=IMAGE_HELP)


def _stream(block):
    return StreamField([("item", block)], blank=True)


class TerritoryPage(PictureMixin, Page):
    @property
    def image(self):
        return self.tile_image

    name = models.CharField(max_length=100)
    picture = picture_field()
    tile_image = models.CharField(max_length=255, blank=True, help_text=IMAGE_HELP)
    hero_picture = picture_field()
    hero_image = models.CharField(max_length=255, blank=True, help_text=IMAGE_HELP)
    employers = models.PositiveIntegerField(default=5)
    highlights = _stream(HighlightBlock())
    assets_title = models.CharField(max_length=200, blank=True)
    assets = _stream(AssetBlock())
    state_title = models.CharField(max_length=200, blank=True)
    state_text = models.TextField(blank=True)
    state_links = StreamField([("item", blocks.CharBlock())], blank=True)
    figures_title = models.CharField(max_length=200, blank=True)
    figures = _stream(FigureBlock())
    links_title = models.CharField(max_length=200, blank=True)
    links = _stream(LinkBlock())

    parent_page_types = ["editorial.TerritoryIndexPage"]
    subpage_types: list[str] = []
    template = "pages/territory.html"
    content_panels = [
        *Page.content_panels,
        FieldPanel("name"),
        FieldPanel("picture"),
        FieldPanel("tile_image"),
        FieldPanel("hero_picture"),
        FieldPanel("hero_image"),
        FieldPanel("employers"),
        FieldPanel("highlights"),
        FieldPanel("assets_title"),
        FieldPanel("assets"),
        FieldPanel("state_title"),
        FieldPanel("state_text"),
        FieldPanel("state_links"),
        FieldPanel("figures_title"),
        FieldPanel("figures"),
        FieldPanel("links_title"),
        FieldPanel("links"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["territory"] = {
            "name": self.name,
            "title": self.title,
            "image": resolve_image(self.hero_picture, self.hero_image)
            or self.display_image,
            "highlights": [
                {
                    "title": b.value["title"],
                    "tags": list(b.value["tags"]),
                    "date": b.value["date"],
                    "image": resolve_image(b.value["picture"], b.value["image"]),
                }
                for b in self.highlights
            ],
            "assets_title": self.assets_title,
            "assets": [
                {
                    **b.value,
                    "image": resolve_image(b.value["picture"], b.value["image"]),
                }
                for b in self.assets
            ],
            "state_title": self.state_title,
            "state_text": self.state_text,
            "state_links": [b.value for b in self.state_links],
            "figures_title": self.figures_title,
            "figures": [(b.value["value"], b.value["label"]) for b in self.figures],
            "employers": self.employers,
            "links_title": self.links_title,
            "links": [
                {
                    **b.value,
                    "image": resolve_image(b.value["picture"], b.value["image"]),
                }
                for b in self.links
            ],
        }
        context["offers_count"] = sum(o["region"] == self.name for o in OFFERS)
        context["breadcrumb_data"] = {"links": [], "current": self.name}
        return context
