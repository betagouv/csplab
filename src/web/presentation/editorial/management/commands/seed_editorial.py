from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from wagtail.models import GroupPagePermission, Site

from presentation.editorial import seed_data
from presentation.editorial.models import (
    AdviceIndexPage,
    AdvicePage,
    AdviceTheme,
    NewsIndexPage,
    NewsPage,
    TerritoryIndexPage,
    TerritoryPage,
)

_PAGE_PERMISSIONS = ("add_page", "change_page", "publish_page", "bulk_delete_page")


def _get_or_add(parent, model, slug, **fields):
    existing = parent.get_children().filter(slug=slug).first()
    if existing:
        return existing, False
    page = model(slug=slug, **fields)
    parent.add_child(instance=page)
    return page, True


class Command(BaseCommand):
    help = "Crée les pages éditoriales (actualités, conseils, territoires)."

    def handle(self, *args, **options):
        home = Site.objects.get(is_default_site=True).root_page
        news_index, _ = _get_or_add(
            home, NewsIndexPage, "actualites", title="Actualités"
        )
        advice_index, _ = _get_or_add(
            home, AdviceIndexPage, "conseils", title="Conseils"
        )
        territory_index, _ = _get_or_add(
            home, TerritoryIndexPage, "territoire", title="Territoires"
        )
        self._news(news_index)
        self._advice(advice_index)
        self._territories(territory_index)
        self._editors_group([news_index, advice_index, territory_index])
        self.stdout.write(self.style.SUCCESS("Contenu éditorial créé."))

    def _news(self, index):
        items = [(n, True) for n in seed_data._FEATURED_NEWS] + [
            (n, False) for n in seed_data._NEWS
        ]
        for position, (item, featured) in enumerate(items, start=1):
            _get_or_add(
                index,
                NewsPage,
                f"actualite-{position}",
                title=item["title"],
                badge=item["badge"],
                description=item.get("description", ""),
                image=item["image"],
                external_url=item["url"],
                featured=featured,
            )

    def _advice(self, index):
        themes = {
            slug: AdviceTheme.objects.get_or_create(
                slug=slug, defaults={"label": label}
            )[0]
            for slug, label in seed_data._ADVICE_THEMES.items()
        }
        for position, item in enumerate(seed_data._ADVICE, start=1):
            page, created = _get_or_add(
                index,
                AdvicePage,
                f"conseil-{position}",
                title=item["title"],
                text=item["text"],
                image=seed_data._ADVICE_IMG + item["image"],
                external_url=seed_data._ADVICE_URL,
            )
            if created:
                page.themes.set([themes[slug] for slug in item["themes"]])
                page.save()

    def _territories(self, index):
        for name, slug in seed_data._TERRITORIES:
            full = seed_data._TERRITORY_PAGES.get(slug, {})
            fields = {
                "title": full.get("title", f"La région {name}"),
                "name": name,
                "tile_image": f"{seed_data._IMG}territories/{slug}.png",
                "hero_image": full.get("image", ""),
                "employers": full.get("employers", 5),
                "assets_title": full.get("assets_title", ""),
                "state_title": full.get("state_title", ""),
                "state_text": full.get("state_text", ""),
                "figures_title": full.get("figures_title", ""),
                "links_title": full.get("links_title", ""),
                "highlights": [("item", h) for h in full.get("highlights", [])],
                "assets": [("item", a) for a in full.get("assets", [])],
                "state_links": [("item", s) for s in full.get("state_links", [])],
                "figures": [
                    ("item", {"value": value, "label": label})
                    for value, label in full.get("figures", [])
                ],
                "links": [("item", link) for link in full.get("links", [])],
            }
            _get_or_add(index, TerritoryPage, slug, **fields)

    def _editors_group(self, indexes):
        group, _ = Group.objects.get_or_create(name="Rédacteur")
        group.permissions.add(
            Permission.objects.get(
                content_type__app_label="wagtailadmin", codename="access_admin"
            )
        )
        for index in indexes:
            for codename in _PAGE_PERMISSIONS:
                GroupPagePermission.objects.get_or_create(
                    group=group,
                    page=index,
                    permission=Permission.objects.get(
                        content_type__app_label="wagtailcore", codename=codename
                    ),
                )
