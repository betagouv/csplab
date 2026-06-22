import re

import markdown
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView


def _wrap_dsfr_tables(html: str) -> str:
    html = re.sub(
        r"<table>",
        '<div class="fr-table"><div class="fr-table__wrapper">'
        '<div class="fr-table__container"><div class="fr-table__content"><table>',
        html,
    )
    return html.replace("</table>", "</table></div></div></div></div>")


def _add_dsfr_heading_classes(html: str) -> str:
    return re.sub(r"<h([1-3])([^>]*)>", r'<h\1\2 class="fr-h\1">', html)


def _add_dsfr_hr_class(html: str) -> str:
    return html.replace("<hr />", '<hr class="fr-hr fr-my-4w" />')


def _strip_sommaire_section(markdown_text: str) -> str:
    return re.sub(
        r"^## Sommaire\n.*?\n---\n",
        "",
        markdown_text,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )


def _toc_to_sidemenu_items(tokens: list[dict]) -> list[dict]:
    return [
        {
            "label": token["name"],
            "link": f"#{token['id']}",
            **(
                {"items": _toc_to_sidemenu_items(token["children"])}
                if token["children"]
                else {}
            ),
        }
        for token in tokens
    ]


class HomeView(TemplateView):
    template_name = "pages/home.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"


class AccessibilityView(TemplateView):
    template_name = "pages/accessibility.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"


class LegalNoticesView(TemplateView):
    template_name = "pages/legal_notices.html"


class ApiGuideView(TemplateView):
    template_name = "pages/api_guide.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        markdown_text = _strip_sommaire_section(
            (settings.STATIC_DIR / "api" / "guide_api.md").read_text()
        )
        md = markdown.Markdown(
            extensions=["tables", "fenced_code", "toc"],
            extension_configs={"toc": {"toc_depth": "1-3"}},
        )
        html = _add_dsfr_heading_classes(md.convert(markdown_text))
        html = _add_dsfr_hr_class(html)
        context["content"] = _wrap_dsfr_tables(html)
        context["toc_items"] = _toc_to_sidemenu_items(md.toc_tokens)
        return context


def security_txt(request):
    content = (
        f"Contact: mailto:{settings.SECURITY_CONTACT_EMAIL}\n"
        "Preferred-Languages: fr, en\n"
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
