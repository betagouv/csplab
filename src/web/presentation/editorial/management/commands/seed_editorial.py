import os
import secrets
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from wagtail.models import (
    Collection,
    GroupCollectionPermission,
    GroupPagePermission,
    Site,
)

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

_PAGE_PERMISSIONS = (
    "add_page",
    "change_page",
    "publish_page",
    "bulk_delete_page",
    "lock_page",
    "unlock_page",
)
_COLLECTION_PERMISSIONS = (
    ("wagtailimages", "add_image"),
    ("wagtailimages", "change_image"),
    ("wagtailimages", "choose_image"),
    ("wagtaildocs", "add_document"),
    ("wagtaildocs", "change_document"),
    ("wagtaildocs", "choose_document"),
)
_SNIPPET_PERMISSIONS = (
    "add_advicetheme",
    "change_advicetheme",
    "delete_advicetheme",
    "view_advicetheme",
)
_CMS_EDITOR_EMAIL = "carine.cms@yopmail.com"


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
        self._territory_editor(
            "normandie",
            "Rédacteur Normandie",
            "antoine.normandie@yopmail.com",
            "Antoine",
            "Normandie",
        )
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
            territory, created = _get_or_add(index, TerritoryPage, slug, **fields)
            if created:
                for news_slug, news in seed_data._TERRITORY_NEWS.get(slug, {}).items():
                    self._territory_news(territory, news_slug, news)

    def _territory_news(self, territory, news_slug, news):
        page, _ = _get_or_add(
            territory,
            NewsPage,
            news_slug,
            title=news["title"],
            badge=news["badge"],
            description=news["description"],
            image=news["image"],
            external_url=news["url"],
        )
        territory.highlights = [
            (
                "item",
                {**block.value, "page": page}
                if block.value["title"] == news["title"]
                else block.value,
            )
            for block in territory.highlights
        ]
        territory.save()

    def _grant(self, group, pages, collection):
        group.permissions.add(
            Permission.objects.get(
                content_type__app_label="wagtailadmin", codename="access_admin"
            )
        )
        for page in pages:
            for codename in _PAGE_PERMISSIONS:
                GroupPagePermission.objects.get_or_create(
                    group=group,
                    page=page,
                    permission=Permission.objects.get(
                        content_type__app_label="wagtailcore", codename=codename
                    ),
                )
        for app_label, codename in _COLLECTION_PERMISSIONS:
            GroupCollectionPermission.objects.get_or_create(
                group=group,
                collection=collection,
                permission=Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                ),
            )

    def _editors_group(self, indexes):
        group, _ = Group.objects.get_or_create(name="Rédacteur")
        self._grant(group, indexes, Collection.get_first_root_node())
        group.permissions.add(
            *Permission.objects.filter(codename__in=_SNIPPET_PERMISSIONS)
        )
        self._staff_user(group, _CMS_EDITOR_EMAIL, "Carine", "Callens")

    def _territory_editor(self, slug, group_name, email, first_name, last_name):
        territory = TerritoryPage.objects.filter(slug=slug).first()
        if territory is None:
            self.stdout.write(
                self.style.WARNING(f"Territoire {slug} introuvable, {email} ignoré.")
            )
            return
        group, _ = Group.objects.get_or_create(name=group_name)
        root = Collection.get_first_root_node()
        collection = root.get_children().filter(name=territory.name).first()
        if collection is None:
            collection = root.add_child(name=territory.name)
        self._grant(group, [territory], collection)
        self._staff_user(group, email, first_name, last_name)

    def _staff_user(self, group, email, first_name, last_name):
        user_model = get_user_model()
        user = user_model.objects.filter(email=email).first()
        if user is None:
            user = user_model.objects.create_user(
                username=uuid4(),
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
            )
            self._set_seed_password(user)
        user.groups.add(group)

    def _set_seed_password(self, user):
        password = os.environ.get("SEED_USER_PASSWORD")
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
            self.stdout.write(f"{user.email} créé, mot de passe de SEED_USER_PASSWORD")
            return
        password = secrets.token_urlsafe(16)
        user.set_password(password)
        user.save(update_fields=["password"])
        self.stdout.write(f"{user.email} créé, mot de passe : {password}")
